import ezr
import step01

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use the acquire function from ezr, which is designed for 
    multi-objective optimization with a limited label budget.
    """
    # Create a table object. Note: rows currently have '?' in goal columns.
    # The label function will be used to fill these in.
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # The acquire function in ezr.py performs active learning to 
    # find the best rows within a budget (the.Stop).
    # We wrap the label function to ensure we track the original indices.
    def oracle_with_index(row):
        # Find the original index of this row in the input list
        idx = rows.index(row)
        # Get the true values
        true_row = label(idx)
        # Update the row in place with true values
        for i in range(len(true_row)):
            row[i] = true_row[i]
        return row

    # Run the acquisition process
    # ezr.acquire returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_with_index)
    
    # Find the best row among those labeled
    # ydist measures distance to the ideal goal values (lower is better)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    # Mask goals for the input rows
    for row in rows:
        for i in range(len(header)):
            if header[i][-1] in "+-":
                row[i] = "?"
                
    # Define the label function for the harness
    # In this context, we know the true values from the original file
    # We reload the file to act as the "oracle"
    full_data = list(ezr.csv(filename))
    full_rows = full_data[1:]
    
    def label(idx):
        return full_rows[idx]
        
    best_idx = choose(header, rows, label)
    
    print(f"Optimization complete.")
    print(f"The best configuration found is at index: {best_idx}")
    print(f"Goal values for this configuration: {full_rows[best_idx][9:]}")
    
    exit(0)
