import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best setup:
    1. 'random': Random sampling.
    2. 'acquire': Intelligent sampling using ezr's acquire.
    3. 'greedy': Picking rows that are closest to the current best-known centroid.
    """
    budget = 50
    tbl = ezr.Tbl([header] + rows)
    
    # Helper to evaluate a row
    def get_ydist(idx):
        row = label(idx)
        return ezr.ydist(tbl, row)

    # 1. Random Strategy
    random_indices = random.sample(range(len(rows)), budget)
    random_results = {idx: get_ydist(idx) for idx in random_indices}
    best_random = min(random_results, key=random_results.get)

    # 2. Acquire Strategy (ezr's built-in)
    # We need to adapt the label function to the oracle signature
    def oracle_wrapper(row):
        # Find index by matching row (assuming unique rows or first match)
        idx = rows.index(row)
        true_vals = label(idx)
        for i, val in enumerate(true_vals):
            if header[i].endswith(('-', '+')):
                row[i] = val
        return row
    
    ezr.the.Stop = budget
    # We use a subset of rows to simulate the training/acquisition process
    labeled_rows = ezr.acquire(tbl, cap=budget, label=oracle_wrapper)
    best_acquire_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    best_acquire = rows.index(best_acquire_row)

    # 3. Greedy Strategy (Pick closest to current best)
    greedy_indices = []
    current_best_idx = random.choice(range(len(rows)))
    greedy_indices.append(current_best_idx)
    
    for _ in range(budget - 1):
        # Find row closest to the current best
        best_row = rows[current_best_idx]
        # Sort remaining by xdist to current best
        remaining = [i for i in range(len(rows)) if i not in greedy_indices]
        next_idx = min(remaining, key=lambda i: ezr.xdist(tbl, rows[i], best_row))
        greedy_indices.append(next_idx)
        if get_ydist(next_idx) < get_ydist(current_best_idx):
            current_best_idx = next_idx
    best_greedy = current_best_idx

    # Compare results
    scores = {
        "random": (best_random, get_ydist(best_random)),
        "acquire": (best_acquire, get_ydist(best_acquire)),
        "greedy": (best_greedy, get_ydist(best_greedy))
    }
    
    winner = min(scores, key=lambda k: scores[k][1])
    
    return {
        "winner": winner,
        "row": scores[winner][0],
        "tried": ["random", "acquire", "greedy"]
    }

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Mask goals
    masked_rows = [[row[i] if not header[i].endswith(('-', '+')) else "?" 
                    for i in range(len(row))] for row in rows]
    
    def label_func(idx):
        return all_data[idx + 1]
    
    result = race(header, masked_rows, label_func)
    
    print("Race Results (50 labels each):")
    print(f"Winner: {result['winner']}")
    print(f"Best row index found: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    exit(0)
