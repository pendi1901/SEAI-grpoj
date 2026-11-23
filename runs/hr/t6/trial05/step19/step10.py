import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies: random, acquire, and greedy.
    Total budget is 50 labels.
    """
    budget = 50
    labeled_cache = {}

    def oracle_wrapper(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    # Create a table using the full rows (with goals) to ensure ydist works
    # We use the first row to infer the structure, then build the table
    tbl = ezr.Tbl([header] + [label(i) for i in range(min(len(rows), 5))])
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))

    # Strategy 2: Acquire (ezr's default)
    def strategy_acquire():
        # We use a subset of the budget
        # We need to pass a function that labels the row
        def label_func(row):
            # Find index of row in original rows list
            idx = rows.index(row)
            return oracle_wrapper(idx)
        
        # We need a table for acquire that has the goal columns populated
        # Since we can't know all goals, we use the ones we have labeled
        labeled_rows = [oracle_wrapper(i) for i in labeled_cache.keys()]
        # If not enough, just use the first few
        if not labeled_rows: labeled_rows = [label(0)]
        
        lab_tbl = ezr.clone(tbl, labeled_rows)
        best_row = min(ezr.acquire(lab_tbl, cap=budget // 3, label=label_func), 
                       key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Strategy 3: Greedy (pick rows with highest xdist from centroid)
    def strategy_greedy():
        centroid = ezr.mids(tbl)
        scored = sorted(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[i], centroid), reverse=True)
        indices = scored[:budget // 3]
        for i in indices: oracle_wrapper(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, oracle_wrapper(i)))

    results = {
        "random": strategy_random(),
        "acquire": strategy_acquire(),
        "greedy": strategy_greedy()
    }

    # Find winner: lowest ydist
    winner = min(results, key=lambda name: ezr.ydist(tbl, oracle_wrapper(results[name])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    masked_rows = []
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)

    def label(i):
        return rows[i]

    result = race(header, masked_rows, label)
    
    print("Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    exit(0)
