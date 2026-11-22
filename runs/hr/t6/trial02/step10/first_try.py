import ezr
import random
import step07

def race(header, rows, label):
    """
    Compare three strategies: random, greedy (acquire), and a hybrid.
    Budget: 50 labels total.
    """
    budget = 50
    # Track which indices have been labeled to respect the 50-label limit
    labeled_cache = {}

    def get_label(i):
        if i not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[i] = label(i)
        return labeled_cache[i]

    # Strategy 1: Random
    def strategy_random(tbl, budget_per):
        indices = random.sample(range(len(rows)), budget_per)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Greedy (using ezr.acquire)
    def strategy_greedy(tbl, budget_per):
        # We use the logic from step07 to pick the best row
        best_idx = step07.choose(header, rows, get_label)
        return best_idx

    # Strategy 3: Exploration (Sample then refine)
    def strategy_explore(tbl, budget_per):
        # Sample half, then focus on the best
        indices = random.sample(range(len(rows)), budget_per)
        for i in indices: get_label(i)
        # Refine: pick the best from the sample and look for its neighbors
        best_i = min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))
        return best_i

    tbl = ezr.Tbl([header] + rows)
    
    # Allocate budget: 16 per strategy (48 total)
    strategies = {
        "random": lambda: strategy_random(tbl, 16),
        "greedy": lambda: strategy_greedy(tbl, 16),
        "explore": lambda: strategy_explore(tbl, 16)
    }

    results = {}
    for name, func in strategies.items():
        try:
            results[name] = func()
        except Exception:
            results[name] = -1

    # Determine winner: lowest ydist
    best_name = min(results, key=lambda n: ezr.ydist(tbl, rows[results[n]]) if results[n] != -1 else 1e30)
    
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
    
    # Mask goals
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
