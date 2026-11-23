import ezr

def choose(header, rows, label):
    """
    Find the best setup by using the acquire strategy from ezr.
    We have a budget of 50 labels.
    """
    # Create a table object. The rows currently have '?' for goals.
    # We need to use the provided label function to fill them in.
    # The acquire function in ezr takes a TBL and an ORACLE.
    # We wrap the provided label function to match the ORACLE signature.
    
    # Create a dummy table to hold the structure
    tbl = ezr.Tbl([header] + rows)
    
    # We need to track which rows we have already labeled to avoid 
    # exceeding the 50-label budget.
    labeled_cache = {}

    def oracle_wrapper(row):
        # Find the index of this row in the original list
        # Since rows are unique in this dataset, we can find by identity
        for i, r in enumerate(rows):
            if r is row:
                if i not in labeled_cache:
                    labeled_cache[i] = label(i)
                # Return the row with goals filled in
                new_row = list(row)
                for j in range(len(labeled_cache[i])):
                    new_row[j] = labeled_cache[i][j]
                return new_row
        return row

    # Use the acquire function to find the best rows within the budget
    # ezr.acquire returns the rows that were labeled and explored
    best_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among those we labeled
    # Sort by ydist (lower is better)
    best_rows.sort(key=lambda r: ezr.ydist(tbl, r))
    best_row = best_rows[0]
    
    # Find the index of this best row in the original rows list
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Mask the goals for the choose function
    masked_rows = []
    for row in all_rows:
        masked_rows.append(["?" if i < 3 else val for i, val in enumerate(row)])
    
    # Define the label function for the harness
    def label_func(i):
        return all_rows[i][:3]
    
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis complete. Best setup found at index: {best_idx}")
    print(f"Best row goals (MRE-, ACC+, PRED40+): {all_rows[best_idx][:3]}")
    
    exit(0)
