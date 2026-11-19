import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, greedy (based on tree), and 
    the built-in acquire (based on distance to best/rest).
    """
    # Shared budget
    budget = 50
    budget_used = 0
    labeled_cache = {}

    def get_label(i):
        nonlocal budget_used
        if i not in labeled_cache:
            if budget_used >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[i] = label(i)
            budget_used += 1
        return labeled_cache[i]

    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices:
            get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Tree-based (Greedy)
    def strategy_tree():
        # Build a tree on a small initial sample
        indices = random.sample(range(len(rows)), 10)
        for i in indices: get_label(i)
        
        # Rank remaining by tree leaf mean
        lab_rows = [rows[i] for i in labeled_cache.keys()]
        lab_tbl = ezr.clone(tbl, lab_rows)
        ranker = ezr.ranker(lab_tbl)
        
        # Pick best remaining
        candidates = [i for i in range(len(rows)) if i not in labeled_cache]
        best_i = min(candidates, key=lambda i: ranker(rows[i]))
        get_label(best_i)
        return best_i

    # Strategy 3: Distance-based (Acquire)
    def strategy_acquire():
        # Use ezr.acquire logic
        # We need to map the oracle to our get_label
        def oracle_wrapper(row):
            # Find index
            for i, r in enumerate(rows):
                if r == row:
                    vals = get_label(i)
                    for j, col in enumerate(tbl.y):
                        row[col.at] = vals[j]
                    return row
            return row
        
        labeled = ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)
        best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Run race
    results = {
        "random": strategy_random(),
        "tree": strategy_tree(),
        "acquire": strategy_acquire()
    }
    
    # Determine winner (lowest ydist)
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "tree", "acquire"]
    }

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    # Hide goals
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    result = race(header, rows, label)
    print(f"Race Results: The winning strategy is '{result['winner']}'.")
    print(f"Best row found at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
