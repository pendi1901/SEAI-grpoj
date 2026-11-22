import ezr
import step01

def choose(header, rows, label):
    """
    Finds the best row by using the acquire logic from ezr.
    We label up to 50 rows, then return the index of the best one found.
    """
    # Create a table object to manage the data
    # We need to handle the fact that rows have '?' in goal columns
    # The label function provides the true values.
    
    # We use ezr.acquire to select rows to label.
    # We need to wrap the label function to work with row indices.
    def oracle_wrapper(row):
        # Find the index of this row in the original list
        # Note: This assumes rows are unique or we just need the index of the first match
        idx = rows.index(row)
        true_values = label(idx)
        # Update the row with true values
        for i, val in enumerate(true_values):
            row[i] = val
        return row

    # Create a table from the rows (with '?' in goals)
    # We need to ensure the table knows about the goals
    tbl = ezr.Tbl([header] + rows)
    
    # Use the acquire logic to pick and label rows
    # ezr.acquire returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    # A row is better if it has a lower ydist
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Keep a copy of original rows to look up true values
    original_rows = [list(r) for r in rows]
    
    # Mask the goals
    goal_indices = [i for i, h in enumerate(header) if h[-1] in "+-"]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    # Define the label function for the harness
    def label(i):
        return original_rows[i]
    
    best_idx = choose(header, rows, label)
    
    print(f"The best setup found is at index {best_idx}.")
    print("Values for the best setup:")
    for h, v in zip(header, original_rows[best_idx]):
        print(f"  {h:25}: {v}")
