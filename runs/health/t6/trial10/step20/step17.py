import ezr
import step01
import step07

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (low ydist) and is small enough to run
    every night (low N_estimators). We define 'small' as having a low 
    N_estimators value. We use the acquire function to explore the space
    and then select the best row based on a multi-objective score that 
    penalizes high N_estimators.
    """
    # Create a table object
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # We need to wrap the label function to handle the row indices.
    # We label at most 50 rows.
    labeled_cache = {}
    def oracle_wrapper(row):
        idx = rows.index(row)
        if idx not in labeled_cache:
            if len(labeled_cache) >= 50:
                return row # Should not happen based on acquire logic
            labeled_cache[idx] = label(idx)
        
        # Update the row in-place with the true values
        for i, val in enumerate(labeled_cache[idx]):
            row[i] = val
        return row

    # Use acquire to explore the space
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the index of N_estimators
    n_est_idx = header.index("N_estimators")
    
    # Find the best row. We want low ydist AND low N_estimators.
    # We normalize N_estimators to 0..1 to balance with ydist.
    all_n = [r[n_est_idx] for r in labeled_rows]
    min_n, max_n = min(all_n), max(all_n)
    
    def score(row):
        yd = ezr.ydist(tbl, row)
        # Normalize N_estimators: lower is better
        n_norm = (row[n_est_idx] - min_n) / (max_n - min_n + 1e-32)
        # Combine: 70% weight on performance (ydist), 30% on smallness
        return 0.7 * yd + 0.3 * n_norm

    best_row = min(labeled_rows, key=score)
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i):
        return rows[i]
    
    best_idx = choose(header, masked_rows, label)
    
    print(f"Optimization complete.")
    print(f"The best configuration found for performance and efficiency is at index {best_idx}.")
    print(f"Row details: {rows[best_idx]}")
