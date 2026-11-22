import ezr
import random
import step07

def race(header, rows, label):
    """
    Compares three strategies for finding the best setup within a 50-label budget.
    Strategies:
    1. random: Picks rows at random.
    2. acquire: Uses ezr's active learning (from step07).
    3. greedy: Picks rows that are closest to the current best known row in input space.
    """
    budget = 50
    labeled_count = 0
    memo = {}

    def get_label(idx):
        nonlocal labeled_count
        if idx not in memo:
            if labeled_count >= budget:
                raise Exception("Budget exceeded")
            memo[idx] = label(idx)
            labeled_count += 1
        return memo[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget)
        for i in indices: get_label(i)
        return min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Acquire (from step07)
    def strategy_acquire():
        # Re-use logic from step07, but pass our controlled labeler
        def local_label(idx):
            return get_label(idx)
        return step07.choose(header, rows, local_label)

    # Strategy 3: Greedy (Nearest Neighbor to current best)
    def strategy_greedy():
        # Start with one random label
        start_idx = random.randint(0, len(rows) - 1)
        get_label(start_idx)
        
        while labeled_count < budget:
            # Find best labeled so far
            best_idx = min(memo.keys(), key=lambda i: ezr.ydist(tbl, rows[i]))
            # Find nearest unlabelled
            unlabelled = [i for i in range(len(rows)) if i not in memo]
            if not unlabelled: break
            next_idx = min(unlabelled, key=lambda i: ezr.xdist(tbl, rows[i], rows[best_idx]))
            get_label(next_idx)
        return min(memo.keys(), key=lambda i: ezr.ydist(tbl, rows[i]))

    tbl = ezr.Tbl([header] + rows)
    
    results = {}
    # Run strategies
    for name, func in [("random", strategy_random), ("acquire", strategy_acquire), ("greedy", strategy_greedy)]:
        memo.clear()
        labeled_count = 0
        best_idx = func()
        results[name] = (best_idx, ezr.ydist(tbl, rows[best_idx]))

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
