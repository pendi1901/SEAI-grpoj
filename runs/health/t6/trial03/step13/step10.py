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
    
    # We need a table that has the full data to calculate ydist correctly.
    # Since the harness provides rows with '?', we must fill them using the label function
    # before calculating ydist, or use a table that has been updated.
    full_data = [header] + [list(r) for r in rows]
    tbl = ezr.Tbl(full_data)
    
    # Reset the table to have no rows so we can add them as we label
    tbl = ezr.clone(tbl, [])

    memo = {}
    labeled_count = 0

    def get_label(idx):
        nonlocal labeled_count
        if idx not in memo:
            if labeled_count >= budget:
                raise Exception("Budget exceeded")
            goals = label(idx)
            row = list(rows[idx])
            # Update row with true goals
            for i, col in enumerate(header):
                if col[-1] in "+-":
                    row[i] = goals.pop(0)
            memo[idx] = row
            ezr.addRow(tbl, row)
            labeled_count += 1
        return memo[idx]

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), budget)
        for i in indices: get_label(i)
        return min(memo.keys(), key=lambda i: ezr.ydist(tbl, memo[i]))

    # Strategy 2: Acquire
    def strategy_acquire():
        # Re-use logic from step07, but pass our controlled labeler
        def local_label(idx):
            return get_label(idx)
        # step07.choose expects masked rows
        masked = [list(r) for r in rows]
        for r in masked:
            for i, col in enumerate(header):
                if col[-1] in "+-": r[i] = "?"
        return step07.choose(header, masked, lambda i: label(i))

    # Strategy 3: Greedy
    def strategy_greedy():
        start_idx = random.randint(0, len(rows) - 1)
        get_label(start_idx)
        while labeled_count < budget:
            best_idx = min(memo.keys(), key=lambda i: ezr.ydist(tbl, memo[i]))
            unlabelled = [i for i in range(len(rows)) if i not in memo]
            if not unlabelled: break
            # Find nearest unlabelled to the best labeled row
            next_idx = min(unlabelled, key=lambda i: ezr.xdist(tbl, rows[i], memo[best_idx]))
            get_label(next_idx)
        return min(memo.keys(), key=lambda i: ezr.ydist(tbl, memo[i]))

    results = {}
    for name, func in [("random", strategy_random), ("acquire", strategy_acquire), ("greedy", strategy_greedy)]:
        memo.clear()
        labeled_count = 0
        tbl.rows = []
        tbl.mids = None
        for c in tbl.cols.values():
            c.n = 0
            if hasattr(c, 'mu'): c.mu = c.m2 = c.sd = 0
            else: c.has = {}
        
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
