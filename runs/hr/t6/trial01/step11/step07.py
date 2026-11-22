import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement using at most 50 labels.
    We use the acquire() function from ezr, which is designed to 
    spend a label budget to find the best rows.
    """
    # Create a table object. The goals are currently '?' in the rows
    # provided by the harness, but ezr.Tbl expects the structure.
    # We create a dummy table to hold the data.
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function uses the budget (the.Stop) to label rows
    # and returns the rows that were labeled.
    # We define a wrapper for the label function to match the expected signature.
    def oracle_wrapper(row):
        # Find the index of this row in the original list to call label()
        # The harness expects an index. We find the row by matching content.
        for i, r in enumerate(rows):
            if r == row:
                true_vals = label(i)
                # Update the row with the true values
                for j, col in enumerate(tbl.y):
                    row[col.at] = true_vals[j]
                return row
        return row

    # Use ezr.acquire to find the best rows within the budget
    # the.Stop is set to 50 by default in ezr.py
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    # A row is better if its ydist is lower
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Prepare rows by hiding goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    hidden_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        hidden_rows.append(new_row)
        
    # Define the label function for the harness
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    # Run the selection
    best_idx = choose(header, hidden_rows, label)
    
    print(f"Analysis: Best working arrangement found at index {best_idx}.")
    print(f"Details of the best row:")
    for i, val in enumerate(rows[best_idx]):
        print(f"  {header[i]}: {val}")
