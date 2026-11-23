import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies: random, greedy, and tree-based.
    The shared budget of 50 labels is strictly enforced.
    """
    budget = 50
    labeled_data = {} # index -> row (with goals filled)

    def get_label(i):
        if i not in labeled_data:
            if len(labeled_data) >= budget:
                return None
            true_vals = label(i)
            row = list(rows[i])
            for j, val in enumerate(true_vals):
                row[j] = val
            labeled_data[i] = row
        return labeled_data[i]

    # Helper to calculate ydist for a row that might have '?'
    def get_ydist(i):
        row = get_label(i)
        if not row: return 1e30
        # Create a temporary table to get correct normalization for this row
        # based on the current knowledge
        temp_tbl = ezr.Tbl([header] + [r for r in labeled_data.values()])
        return ezr.ydist(temp_tbl, row)

    # Strategy 1: Random
    def strategy_random():
        indices = random.sample(range(len(rows)), 50)
        for i in indices:
            get_label(i)

    # Strategy 2: Greedy (Nearest to best)
    def strategy_greedy():
        # Start with 5 random
        for i in random.sample(range(len(rows)), 5):
            get_label(i)
        # Hill climb
        while len(labeled_data) < 50:
            best_i = min(labeled_data.keys(), key=get_ydist)
            # Find unlabelled row closest to current best
            unlabeled = [i for i in range(len(rows)) if i not in labeled_data]
            if not unlabeled: break
            # Use xdist to find nearest neighbor
            tbl = ezr.Tbl([header] + [r for r in labeled_data.values()])
            next_i = min(unlabeled, key=lambda i: ezr.xdist(tbl, rows[i], labeled_data[best_i]))
            get_label(next_i)

    # Strategy 3: Tree-based
    def strategy_tree():
        # Use ezr.acquire logic
        tbl = ezr.Tbl([header] + rows)
        def oracle_wrapper(row):
            # Find index
            for i, r in enumerate(rows):
                if r is row:
                    return get_label(i)
            return row
        ezr.acquire(tbl, cap=50, label=oracle_wrapper)

    # Run the race
    # We must reset labeled_data for each strategy to ensure fair budget usage
    results = {}
    strategies = {"random": strategy_random, "greedy": strategy_greedy, "tree": strategy_tree}
    
    for name, func in strategies.items():
        labeled_data = {}
        func()
        if labeled_data:
            best_i = min(labeled_data.keys(), key=get_ydist)
            results[name] = (best_i, get_ydist(best_i))
        else:
            results[name] = (-1, 1e30)

    winner = min(results, key=lambda n: results[n][1])
    return {"winner": winner, "row": results[winner][0], "tried": list(strategies.keys())}

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    all_rows = list(rows_gen)
    
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    masked_rows = []
    for r in all_rows:
        new_row = list(r)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label_func(i):
        return all_rows[i]
    
    random.seed(1234567891)
    result = race(header, masked_rows, label_func)
    
    print(f"Race Results:")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
