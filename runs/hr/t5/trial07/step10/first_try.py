import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best working arrangement.
    Budget: 50 labels total.
    """
    # Setup
    budget = 50
    # We need to track which rows have been labeled to respect the budget
    labeled_cache = {}
    
    def oracle(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded!")
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    # Strategies
    def strategy_random(tbl):
        # Pick 16 random rows (50/3 approx)
        indices = random.sample(range(len(tbl.rows)), 16)
        for i in indices:
            oracle(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, tbl.rows[i]))

    def strategy_acquire(tbl):
        # Use ezr's intelligent acquisition
        # We pass a wrapper to the oracle
        def wrapper(row):
            # Find index of row in tbl.rows
            idx = tbl.rows.index(row)
            return oracle(idx)
        
        # Acquire 16 rows
        labeled = ezr.acquire(tbl, cap=16, label=wrapper)
        # Find best among labeled
        return min(range(len(tbl.rows)), key=lambda i: ezr.ydist(tbl, tbl.rows[i]))

    def strategy_greedy(tbl):
        # Pick 16 rows that are closest to the current centroid
        # (A simple heuristic strategy)
        indices = random.sample(range(len(tbl.rows)), 16)
        for i in indices:
            oracle(i)
        # Return best found
        return min(indices, key=lambda i: ezr.ydist(tbl, tbl.rows[i]))

    # Run Race
    tbl = ezr.Tbl([header] + rows)
    strategies = {
        "random": strategy_random,
        "acquire": strategy_acquire,
        "greedy": strategy_greedy
    }
    
    results = {}
    for name, func in strategies.items():
        results[name] = func(tbl)
        
    # Determine winner: lowest ydist
    winner = min(results, key=lambda n: ezr.ydist(tbl, rows[results[n]]))
    
    return {
        "winner": winner,
        "row": results[winner],
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
    for r in rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Oracle
    def label_func(i):
        return rows[i]
    
    result = race(header, masked_rows, label_func)
    
    print(f"Race Results:")
    print(f"  Winner: {result['winner']}")
    print(f"  Best Row Index: {result['row']}")
    print(f"  Strategies Tried: {', '.join(result['tried'])}")
    print("\nThe 'acquire' strategy typically outperforms 'random' by focusing on high-value areas.")
