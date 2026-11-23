import ezr
import random

def choose(header, rows, label):
    """
    Uses the acquire function from ezr to find the best row within a 50-label budget.
    The acquire function uses a small initial sample and then iteratively 
    labels rows that are far from the 'rest' and near the 'best' centroids.
    """
    # Create a table object. Note: rows currently have '?' in goal columns.
    # The label function provided by the harness will fill these in.
    tbl = ezr.Tbl([header] + rows)
    
    # We need to wrap the label function to handle the index-based requirement.
    # The oracle expects a row, but the harness provides a label(index) function.
    def oracle(row):
        # Find the index of this row in the original list to call label(i)
        # Since rows are passed by reference, we can find the index.
        idx = rows.index(row)
        true_row = label(idx)
        # Update the row in place with the true values
        for i, val in enumerate(true_row):
            row[i] = val
        return row

    # Use ezr.acquire to perform the active learning search.
    # It will call oracle() at most 50 times.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Find the best row among the labeled ones based on ydist
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goal columns for the input to choose()
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label_func(i):
        return rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Best employee arrangement found at index: {best_idx}")
    print("This row represents the optimal balance of goals based on 50 targeted interviews.")
