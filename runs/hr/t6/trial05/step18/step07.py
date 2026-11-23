import ezr
import random

def choose(header, rows, label):
    """
    Finds the best row by using the 'acquire' strategy from ezr.
    We label up to 50 rows, then return the index of the best one found.
    """
    # Create a table object. 
    # We must ensure the table is initialized with the header and rows.
    # The error occurred because the rows passed to Tbl had '?' in goal columns,
    # but the column definitions in Tbl were expecting valid data.
    # Since ezr.Tbl expects rows to be fully populated to calculate initial mids,
    # we provide a dummy row or handle the '?' in the oracle.
    # However, the simplest fix is to initialize the table with the rows 
    # and ensure the oracle fills them correctly.
    tbl = ezr.Tbl([header] + rows)
    
    # Track which rows have been labeled to avoid re-labeling
    labeled_data = {}

    def oracle_wrapper(row):
        # Find the index of this row in the original list to call label()
        # We use the row object identity to find the index.
        idx = rows.index(row)
        if idx not in labeled_data:
            labeled_data[idx] = label(idx)
        return labeled_data[idx]

    # Use ezr.acquire to intelligently select rows to label.
    # We pass the table and the oracle.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among those we labeled.
    # We use ydist to determine the best row (lowest ydist is best).
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    return rows.index(best_row)

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Create a copy of rows with goals masked as '?'
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label(i):
        return rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label)
    
    # Print result
    print(f"Best employee arrangement found at index: {best_idx}")
    print("This row was identified using 50 targeted interviews.")
    print(f"Goal metrics (tenure/role duration) for this row: {rows[best_idx][-4:]}")
    
    exit(0)
