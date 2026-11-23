import ezr
import step01

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use the acquire function from ezr, which is designed for 
    multi-objective optimization with a limited label budget.
    """
    # Create a table object. The rows currently have '?' in goal columns.
    # We need to provide a wrapper for the label function that 
    # updates the rows in our table as we query them.
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr.py takes a TBL and an ORACLE.
    # We define an oracle that calls the provided label function
    # and updates the internal state of our table.
    def oracle_wrapper(row):
        # Find the index of this row in the original list to get the label
        # Since rows are passed by reference, we find the index by matching
        idx = -1
        for i, r in enumerate(rows):
            if r is row:
                idx = i
                break
        
        if idx != -1:
            true_goals = label(idx)
            # Update the row with true values
            for i in range(len(true_goals)):
                row[9 + i] = true_goals[i]
            # Update the table's column stats
            ezr.addCols(tbl, row)
        return row

    # Use ezr.acquire to perform the search.
    # It will use the budget defined in ezr.the.Stop (default 50).
    # It returns the rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among all rows that have been labeled.
    # We calculate ydist for all rows that now have values.
    best_row = None
    best_ydist = 1e30
    best_idx = -1
    
    for i, row in enumerate(rows):
        # Check if row is fully labeled (no '?')
        if "?" not in row[9:]:
            d = ezr.ydist(tbl, row)
            if d < best_ydist:
                best_ydist = d
                best_row = row
                best_idx = i
                
    return best_idx

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the choose function
    for r in rows:
        r[9] = r[10] = r[11] = "?"
        
    # Define the label function for the harness
    # In this context, we simulate the oracle by looking at the original data
    # (which we have access to in this script)
    full_data = list(ezr.csv(filename))
    full_rows = full_data[1:]
    
    def label_func(i):
        return [full_rows[i][9], full_rows[i][10], full_rows[i][11]]
    
    best_idx = choose(header, rows, label_func)
    
    print(f"Best row found at index: {best_idx}")
    print(f"Row values: {rows[best_idx]}")
    exit(0)
