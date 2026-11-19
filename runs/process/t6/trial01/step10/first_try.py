import ezr
import random
import step01
import step07

def race(header, rows, label):
    """
    Compare three strategies: random, tree-based (acquire), and a simple 
    distance-based heuristic. Budget is 50 labels total.
    """
    # Shared budget management
    labeled_indices = {}

    def oracle_wrapper(i):
        if i not in labeled_indices:
            labeled_indices[i] = label(i)
        return labeled_indices[i]

    # Strategy 1: Random
    def strategy_random(tbl, budget):
        indices = random.sample(range(len(tbl.rows)), min(budget, len(tbl.rows)))
        for i in indices: oracle_wrapper(i)
        return min(range(len(tbl.rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 2: Tree-based (using ezr.acquire)
    def strategy_tree(tbl, budget):
        # We need to map the acquire logic to our oracle
        def local_oracle(row):
            # Find index of row
            for i, r in enumerate(rows):
                if r is row: return oracle_wrapper(i)
            return row
        
        best_rows = ezr.acquire(tbl, cap=budget, label=local_oracle)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Strategy 3: Distance-based (Greedy search from a random start)
    def strategy_greedy(tbl, budget):
        curr = random.randint(0, len(rows) - 1)
        oracle_wrapper(curr)
        for _ in range(budget - 1):
            # Find nearest neighbor among unlabelled
            best_n = -1
            min_d = 1e30
            for i in range(len(rows)):
                if i not in labeled_indices:
                    d = ezr.xdist(tbl, rows[curr], rows[i])
                    if d < min_d: min_d, best_n = d, i
            if best_n == -1: break
            curr = best_n
            oracle_wrapper(curr)
        return min(range(len(rows)), key=lambda i: ezr.ydist(tbl, rows[i]))

    # Run the race
    tbl = ezr.Tbl([header] + rows)
    budget_per = 16 # 50 / 3 = 16.6
    
    results = {
        "random": strategy_random(tbl, budget_per),
        "tree": strategy_tree(tbl, budget_per),
        "greedy": strategy_greedy(tbl, budget_per)
    }
    
    # Determine winner (lowest ydist)
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    
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

    # Hide goals
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
