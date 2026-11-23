import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by using the acquire strategy from ezr.
    We have a budget of 50 labels.
    """
    # Create a table object to manage the data.
    # We must ensure the table knows about the columns before we start.
    # We use a copy of the rows to avoid modifying the original list structure
    # while we perform the acquisition.
    tbl = ezr.Tbl([header])
    for row in rows:
        tbl.rows.append(row)
    
    # Re-initialize column stats based on the rows provided
    # (ezr.Tbl constructor already does this, but we ensure it's clean)
    tbl.mids = None
    for row in rows:
        ezr.addCols(tbl, row)

    # Track labeled indices to satisfy the budget constraint
    labeled_data = {}

    def oracle_wrapper(row):
        # Find the index of the row in the original list
        idx = -1
        for i, r in enumerate(rows):
            if r is row:
                idx = i
                break
        
        if idx != -1 and idx not in labeled_data:
            # Get the true values from the oracle
            true_row = label(idx)
            labeled_data[idx] = true_row
            # Update the row with true values
            for j, val in enumerate(true_row):
                row[j] = val
            # Update the table's column stats with the new information
            ezr.addCols(tbl, row)
        return row

    # Perform acquisition
    # We use the acquire function from ezr.
    # Note: acquire expects the table to have rows populated.
    final_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After acquisition, find the best row among the ones we have labeled
    # The best row is the one with the lowest ydist.
    # We only consider rows that were actually labeled.
    best_row = min(final_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the rows passed to choose()
    # We keep a copy of the ground truth for the label function
    ground_truth = [row[:] for row in rows]
    for row in rows:
        for i, name in enumerate(header):
            if name.endswith(("-", "+")):
                row[i] = "?"
                
    def label_func(i):
        return ground_truth[i]
    
    best_idx = choose(header, rows, label_func)
    
    print(f"Best row found at index: {best_idx}")
    print(f"Row data: {ground_truth[best_idx]}")
    exit(0)
