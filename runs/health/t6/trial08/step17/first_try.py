import ezr
import step07

def choose(header, rows, label):
    """
    Find a setup that forecasts well (low ydist) and is small (low N_estimators).
    We use the acquisition logic to explore the space, then select the best
    row based on a multi-objective score that balances accuracy and size.
    """
    # Create a table to handle column roles and distance calculations
    full_tbl = ezr.Tbl([header] + rows)
    n_est_idx = header.index('N_estimators')
    
    # Map row object id to its index
    row_to_idx = {id(r): i for i, r in enumerate(rows)}
    
    # Oracle wrapper to reveal goals
    def oracle_wrapper(row):
        idx = row_to_idx[id(row)]
        return label(idx)

    # Use acquire to find a good set of candidates within the budget
    labeled_rows = ezr.acquire(full_tbl, cap=50, label=oracle_wrapper)
    
    # Score candidates: balance accuracy (ydist) and size (N_estimators)
    # We normalize N_estimators to 0..1 to match ydist scale
    n_vals = [r[n_est_idx] for r in rows]
    min_n, max_n = min(n_vals), max(n_vals)
    
    def score(row):
        ydist = ezr.ydist(full_tbl, row)
        n_norm = (row[n_est_idx] - min_n) / (max_n - min_n + 1e-32)
        # Minimize both ydist and size
        return ydist + 0.5 * n_norm
    
    best_row = min(labeled_rows, key=score)
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(idx):
        return rows[idx]

    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete.")
    print(f"The best setup that balances accuracy and small size is at index {best_idx} (1-based: {best_idx + 1}).")
    
    exit(0)
