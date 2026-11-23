import ezr
import random

def choose(header, rows, label):
    """
    Finds the best row using a budget of 50 labels.
    We use the 'acquire' strategy from ezr to select the most informative
    rows to label.
    """
    # Create a table object. Note: rows currently have '?' in goal columns.
    # ezr.Tbl will treat '?' as a string, which causes issues in norm().
    # We must ensure the table is initialized with valid numeric data for goals
    # or handle the '?' during the acquisition process.
    # Since we are allowed to label 50 rows, we use the provided label function.
    
    # Create a copy of rows to avoid modifying the input list
    working_rows = [list(r) for r in rows]
    
    # We need a table that knows about the columns.
    # We will use the first row to initialize the table structure, 
    # but we must be careful about the '?' in goal columns.
    # We'll create a dummy table and then populate it as we label.
    tbl = ezr.Tbl([header] + [r for r in working_rows if "?" not in r])
    
    # The oracle needs to update the working_rows and the table
    def oracle(row):
        # Find the index of this row in the working_rows list
        # We use the EmployeeNumber (index 9) as a unique identifier
        idx = next(i for i, r in enumerate(working_rows) if r[9] == row[9])
        true_row = label(idx)
        # Update the row in place
        for i, val in enumerate(true_row):
            working_rows[idx][i] = val
            row[i] = val
        # Update the table's column statistics with the new information
        ezr.addCols(tbl, true_row, 1)
        return row

    # Use the acquire function to label up to 50 rows
    # We pass the working_rows to acquire
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # After labeling, find the best row among those we labeled
    # A row is better if its ydist is lower (closer to goals)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    return next(i for i, r in enumerate(working_rows) if r[9] == best_row[9])

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goal columns to simulate the "unknown" state
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    
    # Keep a copy of the original rows to provide to the label function
    original_rows = [list(r) for r in rows]
    
    # Create the masked rows for the choose function
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function
    def label_func(i):
        return original_rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    # Print the result
    best_row = original_rows[best_idx]
    print(f"Best employee arrangement found at index {best_idx}.")
    print("Goal metrics for this employee:")
    for idx in goal_indices:
        print(f"  {header[idx]}: {best_row[idx]}")
