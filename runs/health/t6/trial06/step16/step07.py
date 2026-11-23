import ezr
import step01
import step02
import step06

def choose(header, rows, label):
    """
    Find the best row by using the acquire strategy from ezr.
    We label up to 50 rows, then return the index of the best one found.
    """
    # Create a table object to manage the data
    # We need to handle the '?' in the goal columns for the initial table
    # but ezr.Tbl expects valid data. We'll use the rows provided.
    # Since the goal cells are '?', we must label them to evaluate them.
    
    # We use the acquire logic: it takes a TBL and an ORACLE.
    # The oracle here is the provided 'label' function.
    # We need to wrap the label function to track indices.
    
    labeled_data = []
    
    # We have a budget of 50. 
    # We will use the acquire strategy to pick which rows to label.
    # First, we need a TBL to run acquire on.
    # Since rows have '?', we create a TBL from the rows that are NOT '?'
    # or just use the provided rows and let the oracle fill them.
    
    # The acquire function in ezr expects a TBL where rows have goals.
    # We will label the first 50 rows to build an initial model,
    # or use the acquire function directly.
    
    # Let's use the acquire function from ezr.
    # We need to pass a TBL that has the structure.
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # The acquire function returns the rows that were labeled.
    # We need to ensure the label function is called correctly.
    def oracle_wrapper(row):
        # Find index of this row in the original list
        idx = rows.index(row)
        labeled_row = label(idx)
        # Update the row in place
        for i, val in enumerate(labeled_row):
            row[i] = val
        return row

    # Run the acquisition strategy
    # ezr.acquire uses the.Stop (default 50)
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
        
        # Mask the goals
        masked_rows = []
        for r in all_rows:
            new_row = list(r)
            for i, name in enumerate(header):
                if name[-1] in "+-":
                    new_row[i] = "?"
            masked_rows.append(new_row)
            
        # Define the label function
        def label(i):
            return all_rows[i]
            
        best_idx = choose(header, masked_rows, label)
        print(f"Best configuration found at index: {best_idx}")
        print(f"Best row values: {all_rows[best_idx]}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
        
    exit(0)
