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
    
    # Global tracker for the 50-label budget
    labeled_indices = {}
    
    def get_label(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= budget:
                return None
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    # Helper to evaluate ydist safely
    def get_ydist(tbl, row, true_vals):
        # Create a temporary row with true values to calculate ydist
        temp_row = list(row)
        for idx, col in enumerate(header):
            if col[-1] in "+-":
                temp_row[idx] = true_vals[idx]
        return ezr.ydist(tbl, temp_row)

    tbl = ezr.Tbl([header] + rows)
    results = {}

    # 1. Random Strategy
    def run_random():
        indices = random.sample(range(len(rows)), budget // 3)
        for i in indices:
            get_label(i)

    # 2. Acquire Strategy
    def run_acquire():
        ezr.the.Stop = budget // 3
        def oracle_wrapper(row):
            # Find index by content
            for i, r in enumerate(rows):
                if r == row:
                    true_vals = get_label(i)
                    if true_vals:
                        new_row = list(row)
                        for col_idx, col in enumerate(header):
                            if col[-1] in "+-":
                                new_row[col_idx] = true_vals[col_idx]
                        return new_row
            return row
        ezr.acquire(tbl, cap=budget // 3, label=oracle_wrapper)

    # 3. Greedy Strategy
    def run_greedy():
        curr = random.choice(range(len(rows)))
        for _ in range(budget // 3):
            get_label(curr)
            best_dist = 1e30
            next_idx = curr
            for i in range(len(rows)):
                if i not in labeled_indices:
                    d = ezr.xdist(tbl, rows[i], rows[curr])
                    if d < best_dist:
                        best_dist = d
                        next_idx = i
            curr = next_idx

    # Execute strategies
    for name, func in [("random", run_random), ("acquire", run_acquire), ("greedy", run_greedy)]:
        labeled_indices.clear()
        func()
        # Find best row found by this strategy
        best_i = min(labeled_indices.keys(), key=lambda i: get_ydist(tbl, rows[i], labeled_indices[i]))
        results[name] = (best_i, get_ydist(tbl, rows[best_i], labeled_indices[best_i]))

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
