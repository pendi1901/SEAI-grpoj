import ezr

def choose(header, rows, label):
    """
    Find the best row by using the acquire logic from ezr.
    We have a budget of 50 labels.
    """
    # The error in the previous version occurred because ezr.Tbl 
    # expects rows to have the same length as the header.
    # We must ensure the rows passed to Tbl are complete.
    # Since we don't have the labels yet, we create a TBL 
    # using only the header and an empty list of rows.
    
    # Create an empty table structure
    tbl = ezr.Tbl([header])
    
    # Add the rows to the table structure without triggering index errors
    # by ensuring they match the header length.
    for r in rows:
        tbl.rows.append(r)
        ezr.addCols(tbl, r)
    
    # The oracle needs to return the full row (with labels)
    # We keep track of the original index to return it later.
    # We map the row content to its index to retrieve the label.
    row_map = {tuple(r): i for i, r in enumerate(rows)}
    
    def oracle(row):
        idx = row_map[tuple(row)]
        full_row = label(idx)
        # Update the row in the table with the real values
        for i, val in enumerate(full_row):
            row[i] = val
        return row

    # Use the acquire function to pick the best rows
    # ezr.acquire returns the rows that were labeled
    ezr.the.Stop = 50
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Find the best row among the labeled ones
    # A row is better if its ydist is lower
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
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
        
    # Define the label function
    def label(i):
        return all_rows[i]
        
    best_idx = choose(header, rows, label)
    print(f"Best row found at index: {best_idx}")
    print(f"Row details: {all_rows[best_idx]}")
