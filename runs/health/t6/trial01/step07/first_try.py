import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by using the acquire logic from ezr.
    We have a budget of 50 labels.
    """
    # Create a table structure to handle the data
    # We need to provide the header and rows to the Tbl constructor
    # Note: The goal columns in 'rows' are '?', so we need to fill them
    # using the provided 'label' function.
    
    # We will track which rows we have labeled to stay within the 50 limit
    labeled_data = []
    
    # We use the acquire logic from ezr. 
    # Since 'acquire' expects a TBL and an oracle, we wrap our label function.
    # The 'rows' passed to choose have '?' in goal columns.
    # We need to create a TBL that knows the column roles.
    
    # Create a dummy table to get column definitions
    # We use the first row (with '?' masked) to initialize the table structure
    tbl = ezr.Tbl([header] + rows)
    
    # We need to perform active learning.
    # The 'acquire' function in ezr takes a TBL and an oracle.
    # Our oracle needs to map the index to the label function.
    
    def oracle(row):
        # Find the index of this row in the original rows list
        # Since rows might be passed around, we match by content
        for i, r in enumerate(rows):
            if r == row:
                return label(i)
        return row

    # Use the acquire function to pick the best rows
    # ezr.acquire returns the rows that were labeled
    # We set the budget to 50
    ezr.the.Stop = 50
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Find the best row among the labeled ones
    # A row is better if its ydist is lower
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    for i, r in enumerate(rows):
        if r == best_row:
            return i
    return 0

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
