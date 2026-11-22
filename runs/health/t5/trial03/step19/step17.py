import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (low ydist) and is small (low N_estimators).
    We use the acquire logic to explore the space, then select the best row
    based on a multi-objective score that balances performance and size.
    """
    # The error in the previous version was due to passing rows with '?' 
    # into Tbl, which causes addCols to fail when it tries to process 
    # the '?' as a numeric value. We must only pass fully labeled rows 
    # to the table used for distance calculations.
    
    # Track labels to ensure we don't exceed 50 unique rows
    labeled_data = {}
    
    def oracle_wrapper(row):
        # Find the original index of this row
        for i, r in enumerate(rows):
            if r is row:
                if i not in labeled_data:
                    if len(labeled_data) >= 50:
                        return row
                    labeled_data[i] = label(i)
                return labeled_data[i]
        return row

    # We need a table to calculate ydist. We will build it incrementally
    # as we label rows, ensuring we only add rows with valid goals.
    tbl = ezr.Tbl([header])
    
    # Use acquire to pick rows to label
    # We pass a dummy table to acquire, but we must ensure the rows 
    # passed to it are valid.
    temp_tbl = ezr.Tbl([header])
    temp_tbl.rows = list(rows)
    
    # Perform acquisition
    labeled_rows = ezr.acquire(temp_tbl, cap=50, label=oracle_wrapper)
    
    # Now build the final table with only the labeled rows
    final_tbl = ezr.Tbl([header] + labeled_rows)
    
    # Define a custom score: 
    # We want low ydist (performance) and low N_estimators (size).
    # N_estimators is at index 3.
    n_est_idx = 3
    
    def combined_score(row):
        # Normalize ydist (0 to 1)
        yd = ezr.ydist(final_tbl, row)
        # Normalize N_estimators (approx 50 to 200)
        ne = (row[n_est_idx] - 50) / (200 - 50)
        # Return a weighted sum (lower is better)
        return 0.7 * yd + 0.3 * ne

    # Find the best row among the ones we labeled
    best_row = min(labeled_rows, key=combined_score)
    
    # Find the index of this best row in the original list
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # The customer's rows have goals masked as "?"
    masked_rows = []
    true_goals = []
    for row in all_rows:
        masked = []
        goals = {}
        for i, val in enumerate(row):
            if header[i].endswith('+') or header[i].endswith('-'):
                masked.append("?")
                goals[i] = val
            else:
                masked.append(val)
        masked_rows.append(masked)
        true_goals.append(goals)

    # Define the label function for the harness
    def label_func(i):
        row = list(masked_rows[i])
        for col_idx, val in true_goals[i].items():
            row[col_idx] = val
        return row

    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis complete.")
    print(f"The best configuration found is at index {best_idx}.")
    print("This configuration balances high forecast accuracy with a small footprint.")
