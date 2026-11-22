import ezr
import random

def race(header, rows, label):
    """
    Compares three strategies for finding the best configuration:
    1. random: Randomly samples the space.
    2. acquire: Uses the active learning approach from ezr.
    3. greedy: Picks rows that are closest to the current best-known configuration.
    """
    budget = 50
    strategies = ["random", "acquire", "greedy"]
    
    # Track labels to ensure we don't exceed 50 unique rows
    labeled_data = {}
    def get_label(i):
        if i not in labeled_data:
            if len(labeled_data) >= budget:
                return None
            labeled_data[i] = label(i)
        return labeled_data[i]

    # Create a table for distance calculations
    # We use the full rows list to build the table structure
    tbl = ezr.Tbl([header] + rows)
    
    results = {}
    
    # 1. Random Strategy (16 labels)
    random_indices = random.sample(range(len(rows)), 16)
    for i in random_indices:
        get_label(i)
    results["random"] = min(random_indices, key=lambda i: ezr.ydist(tbl, get_label(i)))

    # 2. Acquire Strategy (17 labels)
    # We pass a clone of the table to acquire to avoid modifying the original
    # We use a custom oracle that pulls from our labeled_data cache
    def acquire_oracle(r):
        idx = rows.index(r)
        return get_label(idx)
    
    # Use a subset of the rows for the acquire process
    acq_rows = ezr.acquire(tbl, cap=17, label=acquire_oracle)
    best_acq = min(acq_rows, key=lambda r: ezr.ydist(tbl, r))
    results["acquire"] = rows.index(best_acq)

    # 3. Greedy Strategy (17 labels)
    # Start at a random point, then move to the nearest neighbor in input space
    curr_idx = random.choice(range(len(rows)))
    for _ in range(17):
        get_label(curr_idx)
        # Find nearest neighbor in input space that hasn't been fully explored
        best_neighbor = -1
        min_dist = float('inf')
        for i in range(len(rows)):
            if i not in labeled_data:
                d = ezr.xdist(tbl, rows[curr_idx], rows[i])
                if d < min_dist:
                    min_dist = d
                    best_neighbor = i
        if best_neighbor != -1:
            curr_idx = best_neighbor
        else:
            break
    results["greedy"] = curr_idx

    # Determine winner by evaluating the best row found by each strategy
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

    outcome = race(header, masked_rows, label_func)
    print(f"Race Results:")
    print(f"Winner: {outcome['winner']}")
    print(f"Best row found at index: {outcome['row']}")
    print(f"Strategies compared: {', '.join(outcome['tried'])}")
