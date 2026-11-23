import ezr
import random

def choose(header, rows, label):
    """
    Find a setup that forecasts well (low ydist) and is small (low N_estimators).
    We define 'small' as having N_estimators <= 50.
    We use the acquire logic to explore the space, but filter for small setups.
    """
    # Identify indices
    n_est_idx = header.index('N_estimators')
    
    # Filter rows to only consider 'small' ones
    # If no rows are small, we fall back to all rows
    small_indices = [i for i, r in enumerate(rows) if r[n_est_idx] <= 50]
    if not small_indices:
        small_indices = list(range(len(rows)))
        
    # Create a mapping for the oracle
    # The oracle expects an index, so we pass the original index
    def oracle_wrapper(i):
        true_vals = label(i)
        for col_idx, val in enumerate(true_vals):
            rows[i][col_idx] = val
        return rows[i]

    # We use a subset of the data to perform acquisition
    # We want to find the best among the small ones
    # We create a table of the small rows
    small_rows = [rows[i] for i in small_indices]
    tbl = ezr.Tbl([header] + small_rows)
    
    # Use ezr.acquire to spend the budget of 50 labels
    # We map the acquire results back to the original indices
    labeled_rows = ezr.acquire(tbl, cap=50, label=lambda r: oracle_wrapper(rows.index(r)))
    
    # Find the best row among the labeled ones
    # A row is better if its ydist is smaller
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(0)

    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)

    def label(i):
        return all_rows[i]

    random.seed(1234567891)
    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete on {len(all_rows)} records.")
    print(f"The best small configuration found is at index {best_idx}.")
    print(f"Configuration details: {all_rows[best_idx]}")
    
    exit(0)
