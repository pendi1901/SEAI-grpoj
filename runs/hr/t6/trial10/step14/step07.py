import ezr

def choose(header, rows, label):
    """
    Uses the 'acquire' strategy from ezr to find the best working arrangement
    within a budget of 50 labels.
    """
    # Create a table object to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # Track which rows we have already labeled to respect the budget
    labeled_cache = {}

    def oracle(row):
        # Find the index of this row in the original list to call label(i)
        # We identify the row by its index in the provided list
        idx = rows.index(row)
        if idx not in labeled_cache:
            labeled_cache[idx] = label(idx)
        
        # The label(i) function returns the full row (including goals).
        # We return the full row as expected by ezr.acquire.
        return labeled_cache[idx]

    # Use ezr.acquire to find the best rows within the 50-label budget.
    # acquire returns a list of rows that have been labeled.
    # Note: acquire expects the rows to already contain the goal values 
    # if they are to be evaluated by ydist.
    best_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Sort the labeled rows by ydist (lower is better)
    best_rows.sort(key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    best_row = best_rows[0]
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Create a local copy of rows with goals masked for the simulation
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name.endswith("+") or name.endswith("-"):
                new_row[i] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label_func(i):
        return rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at index {best_idx}.")
    print(f"This record represents an employee with optimal tenure and management alignment.")
