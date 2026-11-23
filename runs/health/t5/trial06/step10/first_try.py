import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best setup within a 50-label budget.
    Strategies:
    1. random: Picks rows at random.
    2. acquire: Uses the multi-objective acquisition function.
    3. greedy: Picks rows that are closest to the current known best.
    """
    budget = 50
    tried = ["random", "acquire", "greedy"]
    
    # Shared state for the budget
    labeled_indices = {}
    
    def get_label(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    # 1. Random Strategy
    def strategy_random(tbl):
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices:
            get_label(i)
        return indices

    # 2. Acquire Strategy (using ezr.acquire)
    def strategy_acquire(tbl):
        # We use a subset of the budget
        ezr.the.Stop = budget // 3
        def oracle_wrapper(row):
            for i, r in enumerate(rows):
                if r == row:
                    true_goals = get_label(i)
                    new_row = list(row)
                    for col_idx, col in enumerate(header):
                        if col[-1] in "+-":
                            new_row[col_idx] = true_goals[col_idx]
                    return new_row
            return row
        
        labeled = ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)
        return [i for i, r in enumerate(rows) if r in labeled]

    # 3. Greedy Strategy (pick closest to current best)
    def strategy_greedy(tbl):
        indices = []
        curr = random.choice(range(len(rows)))
        for _ in range(budget // 3):
            get_label(curr)
            indices.append(curr)
            # Find next closest unlabelled
            best_dist = 1e30
            next_idx = curr
            for i in range(len(rows)):
                if i not in labeled_indices:
                    d = ezr.xdist(tbl, rows[i], rows[curr])
                    if d < best_dist:
                        best_dist = d
                        next_idx = i
            curr = next_idx
        return indices

    # Run race
    tbl = ezr.Tbl([header] + rows)
    results = {}
    for name, func in [("random", strategy_random), 
                       ("acquire", strategy_acquire), 
                       ("greedy", strategy_greedy)]:
        labeled_indices.clear()
        func(tbl)
        # Find best row found by this strategy
        best_i = min(labeled_indices.keys(), key=lambda i: ezr.ydist(tbl, rows[i]))
        results[name] = (best_i, ezr.ydist(tbl, rows[best_i]))

    winner = min(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": tried}

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    if not data:
        exit(1)
    header, rows = data[0], data[1:]
    
    def label_func(i):
        return rows[i]
    
    res = race(header, rows, label_func)
    print(f"Race Results:")
    print(f"Winner: {res['winner']}")
    print(f"Best row index found: {res['row']}")
    print(f"Strategies tried: {', '.join(res['tried'])}")
    exit(0)
