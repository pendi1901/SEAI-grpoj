import ezr
import step01

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use the acquire logic from ezr to sample the space effectively.
    """
    # Create a table structure to manage the data
    # We need to ensure the rows have the correct header for ezr.Tbl
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr.py takes a TBL and an ORACLE.
    # It returns a list of rows that have been labeled.
    # We need to map the indices to the rows for the label function.
    # Since acquire works on the rows inside the TBL, we can wrap the label function.
    
    def oracle_wrapper(row):
        # Find the index of this row in the original list to call the provided label
        # We use the row content to find the index
        idx = rows.index(row)
        labeled_row = label(idx)
        # Update the row in place with the new values
        for i, val in enumerate(labeled_row):
            row[i] = val
        return row

    # Use the acquire function to pick and label up to 50 rows
    # ezr.the.Stop is 50 by default
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among the labeled ones
    # A row is better if its ydist is lower
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    return rows.index(best_row)

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the choose function
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label_func(idx):
        return rows[idx]
    
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Best setup found at index: {best_idx}")
    print(f"Goals for this setup: {rows[best_idx][goal_indices[0]:]}")
    exit(0)
