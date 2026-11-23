import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement using a budget of 50 labels.
    We use the 'acquire' strategy from ezr to intelligently select rows.
    The label function provided by the harness takes an index and returns the full row.
    """
    # Create a table object to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # The harness provides a label function that takes an index.
    # We need to map the rows back to their indices to use the label function.
    # Since rows are passed as a list, we can use their position.
    row_to_idx = {id(row): i for i, row in enumerate(rows)}
    
    def oracle(row):
        idx = row_to_idx[id(row)]
        true_row = label(idx)
        # Update the row in place with the true values
        for i in range(len(row)):
            row[i] = true_row[i]
        return row

    # Use ezr.acquire to spend the budget. 
    # It returns the rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Find the best row among the ones we labeled.
    # A row is better if its ydist is lower (closer to 0).
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goal columns for the input to choose()
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # The harness expects label(i) to return the full row
    def label_func(idx):
        return rows[idx]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at record index: {best_idx}")
    print(f"This record has been identified as having the most favorable outcomes "
          f"based on the 50-label budget.")
    
    exit(0)
