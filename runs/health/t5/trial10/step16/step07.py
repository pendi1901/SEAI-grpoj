import ezr
import random

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use the acquire logic from ezr to intelligently sample the space.
    """
    # Create a table object to manage the data.
    # We initialize with the header to set up column roles.
    tbl = ezr.Tbl([header])
    
    # We need to track the indices of rows we have already labeled
    # to ensure we don't exceed the budget of 50.
    labeled_indices = set()
    
    # We need a wrapper for the label function that works with the 
    # acquire logic. The acquire logic expects to receive a row,
    # label it, and return the row with goals filled.
    # Since we need to track indices, we map the row object to its index.
    row_to_idx = {id(r): i for i, r in enumerate(rows)}
    
    def oracle_wrapper(row):
        idx = row_to_idx[id(row)]
        if idx not in labeled_indices:
            labeled_indices.add(idx)
            # Get the true values from the harness
            true_row = label(idx)
            # Update the row in place with the true values
            for i in range(len(true_row)):
                row[i] = true_row[i]
        return row

    # Prepare the rows for the acquire function.
    # We need to pass a list of rows that have '?' in goal columns.
    # We create a copy to avoid modifying the original data prematurely.
    working_rows = []
    for r in rows:
        new_row = list(r)
        # Mask the goals
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        working_rows.append(new_row)
        row_to_idx[id(new_row)] = row_to_idx[id(r)]

    # Use ezr.acquire to get the best rows.
    # We set the budget to 50.
    # The acquire function will call our oracle_wrapper.
    # We pass the table initialized with the header.
    # We need to ensure the table knows about the rows.
    tbl.rows = working_rows
    
    final_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among all labeled ones.
    # We use ydist to evaluate the quality.
    best_row = min(final_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row.
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        data = list(ezr.csv(filename))
        header = data[0]
        rows = data[1:]
        
        # Define the label function for the harness
        # In this local context, we just return the row from the list
        def label(i):
            return rows[i]
            
        best_idx = choose(header, rows, label)
        
        print(f"Analysis complete.")
        print(f"The best setup found is at index: {best_idx}")
        print(f"Row details: {rows[best_idx]}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        exit(1)
    
    exit(0)
