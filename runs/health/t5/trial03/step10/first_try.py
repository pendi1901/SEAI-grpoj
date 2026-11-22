import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best configuration:
    1. random: Randomly samples the space.
    2. acquire: Uses the active learning approach from ezr.
    3. greedy: Picks rows that are closest to the current best-known configuration.
    """
    # Shared budget
    budget = 50
    strategies = ["random", "acquire", "greedy"]
    
    # Helper to track labels
    labeled = {}
    def get_label(i):
        if i not in labeled:
            if len(labeled) >= budget:
                raise Exception("Budget exceeded")
            labeled[i] = label(i)
        return labeled[i]

    results = {}
    tbl = ezr.Tbl([header])
    tbl.rows = rows

    # 1. Random Strategy
    random_indices = random.sample(range(len(rows)), budget // 3)
    for i in random_indices:
        get_label(i)
    results["random"] = min(random_indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # 2. Acquire Strategy (Active Learning)
    # We use a subset of the budget
    subset_rows = ezr.acquire(tbl, cap=budget // 3, label=lambda r: get_label(rows.index(r)))
    best_acq = min(subset_rows, key=lambda r: ezr.ydist(tbl, r))
    results["acquire"] = rows.index(best_acq)

    # 3. Greedy Strategy (Local Search)
    # Start with a random point, then move to the nearest neighbor
    curr_idx = random.choice(range(len(rows)))
    for _ in range(budget // 3):
        get_label(curr_idx)
        # Find nearest neighbor in input space
        best_neighbor = min(range(len(rows)), key=lambda i: ezr.xdist(tbl, rows[curr_idx], rows[i]))
        curr_idx = best_neighbor
    results["greedy"] = curr_idx

    # Determine winner
    winner = min(results, key=lambda s: ezr.ydist(tbl, get_label(results[s])))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": strategies
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Mask goals
    masked_rows = []
    for row in all_rows:
        masked = [("?" if header[i].endswith('+') or header[i].endswith('-') else val) 
                  for i, val in enumerate(row)]
        masked_rows.append(masked)

    def label_func(i):
        return all_rows[i]

    try:
        outcome = race(header, masked_rows, label_func)
        print(f"Race Results:")
        print(f"Winner: {outcome['winner']}")
        print(f"Best row found at index: {outcome['row']}")
        print(f"Strategies compared: {', '.join(outcome['tried'])}")
    except Exception as e:
        print(f"Race failed: {e}")
