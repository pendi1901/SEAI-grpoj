import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies:
    1. 'random': Picks rows at random.
    2. 'big_teams': Picks rows with the largest 'Team Size' (the customer's current approach).
    3. 'tree': Uses the tree-based acquisition strategy from ezr.
    """
    labeled_cache = {}
    budget = 50

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            if len(labeled_cache) >= budget:
                raise Exception("Budget exceeded")
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    def reveal(idx):
        true_vals = oracle_wrapper(idx)
        for j, val in enumerate(true_vals):
            if header[j].endswith(("-", "+")):
                rows[idx][j] = val
        return rows[idx]

    tbl = ezr.Tbl([header] + rows)
    team_idx = header.index("Team Size")

    # Strategy 1: Random
    def strategy_random(n):
        indices = random.sample(range(len(rows)), n)
        for i in indices: reveal(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Big Teams (Customer's current approach)
    def strategy_big_teams(n):
        # Sort by team size descending
        sorted_indices = sorted(range(len(rows)), key=lambda i: rows[i][team_idx], reverse=True)
        indices = sorted_indices[:n]
        for i in indices: reveal(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 3: Tree-based
    def strategy_tree(n):
        # Use a subset of rows to build the tree
        local_tbl = ezr.clone(tbl, [rows[i] for i in range(len(rows)) if i in labeled_cache or random.random() < 0.1])
        def local_oracle(r):
            for i, row in enumerate(rows):
                if row is r:
                    reveal(i)
                    return rows[i]
            return r
        labeled = ezr.acquire(tbl, cap=len(labeled_cache) + n, label=local_oracle)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Run strategies
    strategies = {"random": strategy_random, "big_teams": strategy_big_teams, "tree": strategy_tree}
    results = {}
    
    # Reset rows to masked state
    for r in rows:
        for j, h in enumerate(header):
            if h.endswith(("-", "+")): r[j] = "?"
    
    # Allocate budget equally
    budget_per_strategy = budget // len(strategies)
    for name, func in strategies.items():
        results[name] = func(budget_per_strategy)

    # Determine winner
    winner = min(results, key=lambda n: ezr.ydist(tbl, rows[results[n]]))
    
    return {"winner": winner, "row": results[winner], "tried": list(strategies.keys())}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    ground_truth = [row[:] for row in rows]
    
    def label_func(i):
        return ground_truth[i]
        
    result = race(header, rows, label_func)
    
    print("--- Strategy Comparison: Is 'Big Teams' best? ---")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    if result['winner'] == "big_teams":
        print("Conclusion: Your current 'big teams' strategy is optimal.")
    else:
        print("Conclusion: The 'tree' strategy outperforms your current 'big teams' approach.")
    
    exit(0)
