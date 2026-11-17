import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, greedy (nearest to best), and tree-based.
    Budget: 50 labels total.
    """
    # Setup
    tbl = ezr.Tbl([header] + rows)
    
    def get_goals(idx):
        true_row = label(idx)
        return [true_row[i] for i, name in enumerate(header) if name[-1] in "+-"]

    # Strategies
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), budget)
        for i in indices:
            goals = get_goals(i)
            for col_idx, val in zip([c.at for c in tbl.y], goals):
                rows[i][col_idx] = val
        return indices

    def strategy_greedy(budget):
        # Start with 5 random
        indices = random.sample(range(len(rows)), 5)
        for i in indices:
            goals = get_goals(i)
            for col_idx, val in zip([c.at for c in tbl.y], goals):
                rows[i][col_idx] = val
        
        # Greedy: pick rows closest to the current best
        while len(indices) < budget:
            best_idx = min(indices, key=lambda i: ezr.ydist(tbl, rows[i]))
            # Find unlabelled row closest to best_idx
            unlabelled = [i for i in range(len(rows)) if i not in indices]
            next_i = min(unlabelled, key=lambda i: ezr.xdist(tbl, rows[i], rows[best_idx]))
            indices.append(next_i)
            goals = get_goals(next_i)
            for col_idx, val in zip([c.at for c in tbl.y], goals):
                rows[next_i][col_idx] = val
        return indices

    def strategy_tree(budget):
        # Use ezr.acquire which uses tree-based logic
        # We need to map indices to rows for acquire
        indexed_rows = [row + [i] for i, row in enumerate(rows)]
        new_header = header + ["idxX"]
        
        def wrapped_label(row):
            idx = row[-1]
            goals = get_goals(idx)
            for col_idx, val in zip([c.at for c in tbl.y], goals):
                row[col_idx] = val
            return row

        temp_tbl = ezr.Tbl([new_header] + indexed_rows)
        labeled = ezr.acquire(temp_tbl, cap=budget, label=wrapped_label)
        return [int(r[-1]) for r in labeled]

    # Run race
    results = {}
    for name, func in [("random", strategy_random), ("greedy", strategy_greedy), ("tree", strategy_tree)]:
        # Reset rows for each strategy (mask goals)
        for r in rows:
            for i, h in enumerate(header):
                if h[-1] in "+-": r[i] = "?"
        
        func(50)
        # Find best row found by this strategy
        best_i = min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))
        results[name] = (best_i, ezr.ydist(tbl, rows[best_i]))

    winner = min(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": ["random", "greedy", "tree"]}

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Keep a copy of original rows for the oracle
    full_rows = [list(r) for r in rows]
    
    def oracle(idx):
        return full_rows[idx]
    
    # Mask goals
    for r in rows:
        for i, h in enumerate(header):
            if h[-1] in "+-": r[i] = "?"
            
    res = race(header, rows, oracle)
    print(f"Race Results: {res}")
    print(f"The winner is the '{res['winner']}' strategy, finding the best setup at index {res['row']}.")
