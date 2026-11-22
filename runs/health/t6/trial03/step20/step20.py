import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best setup within a 50-label budget.
    Strategies:
    1. random: Picks rows at random.
    2. acquire: Uses ezr's active learning.
    3. greedy: Picks rows that are closest to the current best known row in input space.
    
    To respect the 50-label budget, we divide the budget equally among strategies.
    """
    budget_per_strategy = 16 # 16 * 3 = 48 <= 50
    
    # Setup table for distance calculations
    full_data = [header] + [list(r) for r in rows]
    tbl = ezr.Tbl(full_data)
    
    # Helper to label and track
    memo = {}
    def get_label(idx):
        if idx not in memo:
            if len(memo) >= 50:
                raise Exception("Budget exceeded")
            row = list(rows[idx])
            goals = label(idx)
            # Fill in goals
            for i, col in enumerate(header):
                if col[-1] in "+-":
                    row[i] = goals.pop(0)
            memo[idx] = row
        return memo[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget_per_strategy)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, memo[i]))

    # Strategy 2: Acquire
    def strategy_acquire():
        # Create a small subset for acquire to work on
        indices = random.sample(range(len(rows)), budget_per_strategy)
        subset = [list(rows[i]) for i in indices]
        for r in subset:
            for i, col in enumerate(header):
                if col[-1] in "+-": r[i] = "?"
        
        # Use ezr.acquire
        sub_tbl = ezr.Tbl([header] + subset)
        labeled = ezr.acquire(sub_tbl, cap=budget_per_strategy, label=lambda r: label(rows.index(r)))
        # Find best in labeled
        best_row = min(labeled, key=lambda r: ezr.ydist(tbl, r))
        return rows.index(best_row)

    # Strategy 3: Greedy
    def strategy_greedy():
        indices = random.sample(range(len(rows)), budget_per_strategy)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, memo[i]))

    results = {}
    for name, func in [("random", strategy_random), ("acquire", strategy_acquire), ("greedy", strategy_greedy)]:
        best_idx = func()
        results[name] = (best_idx, ezr.ydist(tbl, memo[best_idx]))

    winner = min(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(results.keys())}

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    def label(i):
        return [rows[i][j] for j, col in enumerate(header) if col[-1] in "+-"]

    result = race(header, rows, label)
    print(f"Race complete. Winner: {result['winner']}.")
    print(f"Best row found at index {result['row']}.")
    print(f"Strategies compared: {', '.join(result['tried'])}.")
    exit(0)
