import ezr

def choose(header, rows, label):
    """
    Find the best setup by using the acquire logic from ezr.
    We have a budget of 50 labels.
    """
    # Create a table structure to handle column roles and distance calculations
    full_tbl = ezr.Tbl([header] + rows)
    
    # We need to keep track of the original indices to return the correct one.
    # We map the row object id to its index.
    row_to_idx = {id(r): i for i, r in enumerate(rows)}
    
    # The oracle wrapper needs to return the row with its goals filled in.
    # The acquire function expects the label function to return the row with goals.
    def oracle_wrapper(row):
        # Find the index of this row to call the provided label()
        idx = row_to_idx[id(row)]
        # The provided label(i) returns the full row with goals.
        # The harness expects label(i) where i is the index.
        return label(idx)

    # Use ezr.acquire to spend the budget of 50 labels.
    # We pass the full dataset as the table to allow the acquisition logic
    # to sample from the entire space.
    # We must ensure the rows in full_tbl are the ones we pass to acquire.
    labeled_rows = ezr.acquire(full_tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among the ones we labeled.
    # A row is better when its ydist is lower.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(full_tbl, r))
    
    # Return the index of the best row found
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Mask the goals for the choose function
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function that reveals the true goals for a given index
    def label(idx):
        return rows[idx]

    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete. Best setup found at index {best_idx} (1-based: {best_idx + 1}).")
    exit(0)
