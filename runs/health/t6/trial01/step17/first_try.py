import ezr
import step07
import random

def choose(header, rows, label):
    """
    Finds a setup that is both accurate (low ydist) and small (low N_estimators).
    We define 'small' as having a low N_estimators value.
    We use the acquire strategy to find high-performing rows, then filter
    for those that are also computationally efficient.
    """
    # 1. Use the acquire logic to find a set of high-performing rows
    # We use the label function provided to get the true goal values
    # We map rows to indices to track them
    row_map = {tuple(r): i for i, r in enumerate(rows)}
    
    def wrapped_label(row):
        idx = row_map[tuple(row)]
        return label(idx)

    # Create a table for the acquire process
    tbl = ezr.Tbl([header] + rows)
    
    # Limit budget to 50 as per rules
    ezr.the.Stop = 50
    labeled_rows = ezr.acquire(tbl, cap=50, label=wrapped_label)
    
    # 2. Score the labeled rows based on a multi-objective criteria:
    # Accuracy (ydist) AND Efficiency (N_estimators).
    # We want low ydist and low N_estimators.
    n_est_idx = header.index("N_estimators")
    
    def score(row):
        # Normalize ydist (0 to 1)
        y_d = ezr.ydist(tbl, row)
        # Normalize N_estimators (0 to 1)
        # Assuming range 10 to 200 based on dataset
        n_val = row[n_est_idx]
        n_norm = (n_val - 10) / (200 - 10)
        # Combined score: lower is better
        return y_d + (0.5 * n_norm)
    
    best_row = min(labeled_rows, key=score)
    
    return row_map[tuple(best_row)]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Mask the goals for the input to the function
    rows = []
    for row in all_rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name[-1] in "+-!":
                new_row[i] = "?"
        rows.append(new_row)
        
    def label(i):
        return all_rows[i]
        
    best_idx = choose(header, rows, label)
    print(f"Recommended setup found at index: {best_idx}")
    print(f"Row details: {all_rows[best_idx]}")
    print("This setup balances high forecast accuracy with low computational overhead.")
