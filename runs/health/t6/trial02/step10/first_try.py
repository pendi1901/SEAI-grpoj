import ezr
import random
import step01
import step07

def race(header, rows, label):
    """
    Compares three strategies for finding the best setup:
    1. random: Randomly samples rows.
    2. acquire: Uses the ezr.acquire logic (active learning).
    3. greedy: Picks rows based on proximity to the current best-known configuration.
    """
    budget = 50
    per_strategy = budget // 3
    
    # Track labeled rows to ensure we don't exceed the global budget
    labeled_indices = set()
    
    def oracle_wrapper(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= budget:
                raise Exception("Budget exceeded")
            labeled_indices.add(idx)
        return label(idx)

    # Prepare data for strategies
    tbl = ezr.Tbl([header] + rows)
    
    results = {}
    
    # 1. Random Strategy
    random_indices = random.sample(range(len(rows)), per_strategy)
    for i in random_indices:
        oracle_wrapper(i)
    results["random"] = min(random_indices, key=lambda i: ezr.ydist(tbl, rows[i]))
    
    # 2. Acquire Strategy (using ezr.acquire)
    # We create a local copy of rows to mask/unmask
    def acquire_label(row):
        idx = rows.index(row)
        vals = oracle_wrapper(idx)
        for i, v in enumerate(vals): row[i] = v
        return row
    
    acq_rows = ezr.acquire(tbl, cap=per_strategy, label=acquire_label)
    results["acquire"] = rows.index(min(acq_rows, key=lambda r: ezr.ydist(tbl, r)))
    
    # 3. Greedy Strategy (Nearest Neighbor to current best)
    greedy_indices = []
    curr = random.choice(range(len(rows)))
    for _ in range(per_strategy):
        greedy_indices.append(curr)
        oracle_wrapper(curr)
        # Find next best by looking for the closest neighbor in x-space
        curr = min(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[curr], rows[i]))
    results["greedy"] = min(greedy_indices, key=lambda i: ezr.ydist(tbl, rows[i]))
    
    # Determine winner
    winner = min(results, key=lambda name: ezr.ydist(tbl, rows[results[name]]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": ["random", "acquire", "greedy"]
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Mask goals
    original_rows = [list(r) for r in rows]
    for row in rows:
        for i, h in enumerate(header):
            if h[-1] in "+-":
                row[i] = "?"
                
    def label(i):
        return original_rows[i]
    
    outcome = race(header, rows, label)
    print(f"Race Results: {outcome}")
    print(f"The winning strategy was '{outcome['winner']}' which found a top setup at index {outcome['row']}.")
