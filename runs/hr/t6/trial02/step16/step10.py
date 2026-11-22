import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, greedy (acquire), and a hybrid.
    Budget: 50 labels total.
    """
    budget = 50
    labeled_cache = {}

    def get_label(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                return rows[i] # Return masked if budget exhausted
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    tbl = ezr.Tbl([header] + rows)
    
    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 16)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # Strategy 2: Greedy (using ezr.acquire)
    def strategy_greedy():
        # acquire returns rows, we need the index
        best_rows = ezr.acquire(tbl, cap=17, label=lambda r: get_label(rows.index(r)))
        best_row = min(best_rows, key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Strategy 3: Explore (Sample then refine)
    def strategy_explore():
        indices = random.sample(range(len(rows)), 17)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    strategies = {
        "random": strategy_random,
        "greedy": strategy_greedy,
        "explore": strategy_explore
    }

    results = {}
    for name, func in strategies.items():
        results[name] = func()

    # Determine winner: lowest ydist
    best_name = min(results, key=lambda n: ezr.ydist(tbl, get_label(results[n])))
    
    return {
        "winner": best_name,
        "row": results[best_name],
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def oracle(i):
        return rows[i]

    result = race(header, masked_rows, oracle)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    exit(0)
