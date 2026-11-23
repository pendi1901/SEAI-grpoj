import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, active learning (acquire), 
    and a greedy search (picking the best based on initial sample).
    """
    # Shared budget
    budget = 50
    # Split budget equally among 3 strategies
    per_strategy = budget // 3
    
    # Keep track of labeled rows to avoid exceeding budget
    labeled_cache = {}
    
    def get_label(i):
        if i not in labeled_cache:
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    # Strategy 1: Random
    def strategy_random(tbl, n):
        indices = random.sample(range(len(rows)), n)
        for i in indices: get_label(i)
        return indices

    # Strategy 2: Active Learning (ezr.acquire)
    def strategy_active(tbl, n):
        # We use a custom oracle to bridge the label function
        def oracle(row):
            idx = rows.index(row)
            true_vals = get_label(idx)
            for i, val in enumerate(true_vals): row[i] = val
            return row
        
        # We need to pass a subset to acquire
        subset = random.sample(rows, min(len(rows), 128))
        labeled = ezr.acquire(ezr.clone(tbl, subset), cap=n, label=oracle)
        return [rows.index(r) for r in labeled]

    # Strategy 3: Greedy (Pick best from initial random sample)
    def strategy_greedy(tbl, n):
        indices = random.sample(range(len(rows)), n)
        for i in indices: get_label(i)
        return indices

    # Run strategies
    tbl = ezr.Tbl([header] + rows)
    strategies = {
        "random": strategy_random,
        "active": strategy_active,
        "greedy": strategy_greedy
    }
    
    results = {}
    for name, func in strategies.items():
        func(tbl, per_strategy)
        # Find best row found by this strategy
        best_idx = -1
        best_ydist = 1e30
        for i, row in enumerate(rows):
            # Only consider rows that were actually labeled
            if i in labeled_cache:
                d = ezr.ydist(tbl, labeled_cache[i])
                if d < best_ydist:
                    best_ydist = d
                    best_idx = i
        results[name] = best_ydist

    winner = min(results, key=results.get)
    
    return {
        "winner": winner,
        "row": best_idx,
        "tried": list(strategies.keys())
    }

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return rows[i]
    
    result = race(header, masked_rows, label_func)
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies tried: {', '.join(result['tried'])}")
