import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies: random, tree-based (acquire), and a distance-based 
    heuristic. Budget is 50 labels total.
    """
    # Shared budget management
    labeled_indices = {}
    budget_limit = 50

    def oracle_wrapper(i):
        if i not in labeled_indices and len(labeled_indices) < budget_limit:
            labeled_indices[i] = label(i)
        return labeled_indices.get(i, rows[i])

    # We need a table that knows the goal values to calculate ydist.
    # Since we only have partial info, we build a table from the full dataset
    # to get the column statistics (mu, sd) for normalization.
    full_tbl = ezr.Tbl([header] + [list(r) for r in rows])
    
    # Strategy 1: Random
    def strategy_random(budget):
        indices = random.sample(range(len(rows)), min(budget, len(rows) - len(labeled_indices)))
        for i in indices: oracle_wrapper(i)
        return min(range(len(rows)), key=lambda i: ezr.ydist(full_tbl, rows[i]))

    # Strategy 2: Tree-based (using ezr.acquire)
    def strategy_tree(budget):
        # Create a temporary table for acquire
        temp_tbl = ezr.clone(full_tbl, [list(r) for r in rows])
        def local_oracle(row):
            # Find index of row by reference
            for i, r in enumerate(rows):
                if r is row: return oracle_wrapper(i)
            return row
        
        ezr.acquire(temp_tbl, cap=len(labeled_indices) + budget, label=local_oracle)
        return min(range(len(rows)), key=lambda i: ezr.ydist(full_tbl, rows[i]))

    # Strategy 3: Greedy (Distance-based)
    def strategy_greedy(budget):
        curr = random.choice(list(range(len(rows))))
        oracle_wrapper(curr)
        for _ in range(budget - 1):
            best_n = -1
            min_d = 1e30
            for i in range(len(rows)):
                if i not in labeled_indices:
                    d = ezr.xdist(full_tbl, rows[curr], rows[i])
                    if d < min_d: min_d, best_n = d, i
            if best_n == -1: break
            curr = best_n
            oracle_wrapper(curr)
        return min(range(len(rows)), key=lambda i: ezr.ydist(full_tbl, rows[i]))

    # Run the race
    budget_per = 16
    results = {
        "random": strategy_random(budget_per),
        "tree": strategy_tree(budget_per),
        "greedy": strategy_greedy(budget_per)
    }
    
    # Determine winner (lowest ydist)
    winner = min(results, key=lambda name: ezr.ydist(full_tbl, rows[results[name]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)

    # Hide goals for the race
    test_rows = [row[:] for row in all_rows]
    for row in test_rows:
        row[9] = row[10] = row[11] = "?"

    def label_func(i):
        return all_rows[i]

    outcome = race(header, test_rows, label_func)
    
    print(f"Race Results:")
    print(f"Strategies tried: {', '.join(outcome['tried'])}")
    print(f"Winner: {outcome['winner']}")
    print(f"Best row index found: {outcome['row']}")
    
    exit(0)
