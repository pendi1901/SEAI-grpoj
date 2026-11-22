import ezr
import random

def choose(header, rows, label):
    """
    Finds a setup that forecasts well (low ydist) and is small (low N_estimators).
    We use the acquire logic to explore the space, then select the best row
    based on a multi-objective score that balances performance and size.
    """
    # Create a table structure to handle column roles
    tbl = ezr.Tbl([header])
    tbl.rows = list(rows)
    
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

    # Use ezr.acquire to perform the search
    # This explores the space effectively within the 50-label budget
    best_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Define a custom score: 
    # We want low ydist (performance) and low N_estimators (size).
    # N_estimators is at index 3.
    n_est_idx = 3
    
    def combined_score(row):
        # Normalize ydist (0 to 1)
        yd = ezr.ydist(tbl, row)
        # Normalize N_estimators (approx 50 to 200)
        ne = (row[n_est_idx] - 50) / (200 - 50)
        # Return a weighted sum (lower is better)
        return 0.7 * yd + 0.3 * ne

    # Find the best row among the ones we labeled
    best_row = min(best_rows, key=combined_score)
    
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
