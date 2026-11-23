import csv
from step01 import remember
from step07 import choose as base_choose

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing and 'small'.
    We define 'small' as having low N_estimators and low Max_depth.
    We sample 50 rows, label them, and pick the best one that 
    also satisfies a size constraint (below median for N_estimators).
    """
    n_est_idx = header.index('N_estimators')
    
    # 1. Sample 50 rows
    step = len(rows) // 50
    indices_to_test = [i * step for i in range(50)]
    
    # 2. Label and filter for "small" setups
    # We define small as N_estimators <= median of the sampled set
    sampled_rows = []
    for i in indices_to_test:
        goals = label(i)
        row = list(rows[i])
        goal_indices = [idx for idx, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for idx, val in zip(goal_indices, goals):
            row[idx] = val
        sampled_rows.append((row, i))
    
    # Calculate median N_estimators of the sampled set
    n_ests = [r[0][n_est_idx] for r in sampled_rows]
    median_n = sorted(n_ests)[len(n_ests) // 2]
    
    # Filter for small setups
    small_setups = [item for item in sampled_rows if item[0][n_est_idx] <= median_n]
    
    # If no small setups, fall back to all sampled
    candidates = small_setups if small_setups else sampled_rows
    
    # 3. Rank candidates using remember logic
    best_indices = remember(header, [c[0] for c in candidates])
    
    # Return the original index of the best small setup
    return candidates[best_indices[0]][1]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    true_goals = [[r[i] for i in goal_indices] for r in rows]
    
    called_count = 0
    def label(i):
        global called_count
        called_count += 1
        if called_count > 50:
            raise Exception("Budget exceeded!")
        return true_goals[i]

    masked_rows = []
    for r in rows:
        new_r = list(r)
        for i in goal_indices:
            new_r[i] = "?"
        masked_rows.append(new_r)

    best_idx = choose(header, masked_rows, label)
    
    print(f"Search complete. Best small setup found at index {best_idx}.")
    print(f"Setup details: {rows[best_idx]}")
    print("This configuration balances performance with low computational overhead.")
