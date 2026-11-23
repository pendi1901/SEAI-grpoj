import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup by using the acquire strategy to explore the space
    within a budget of 50 labels.
    """
    # Create a table structure to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function from ezr.py implements a multi-objective
    # search that balances exploration and exploitation.
    # It takes a label function and a budget (the.Stop).
    # We set the budget to 50 as requested.
    ezr.the.Stop = 50
    
    # We need to wrap the provided 'label' function to work with the 
    # expected signature of the acquire function.
    # The acquire function expects an oracle that takes a row and returns 
    # a row with the goals filled in.
    def oracle_wrapper(row):
        # Find the index of the row in the original list to call the label function
        # Since rows are passed as lists, we match by content.
        # Note: In a real scenario, we'd track indices, but here we 
        # identify the row by its content to get the true values.
        for i, r in enumerate(rows):
            if r == row:
                true_goals = label(i)
                # Update the row with the true goal values
                new_row = list(row)
                for col_idx, col in enumerate(header):
                    if col[-1] in "+-":
                        new_row[col_idx] = true_goals[col_idx]
                return new_row
        return row

    # Perform the acquisition
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones based on ydist
    # ydist measures how close the goals are to the ideal
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    for i, r in enumerate(rows):
        if r == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    # Define the label function for the harness
    def label_func(i):
        # Return the actual goal values for the row at index i
        return rows[i]

    # Run the choice function
    best_idx = choose(header, rows, label_func)
    
    print(f"Search complete. The best setup found is at index {best_idx}.")
    print(f"Setup details: {rows[best_idx]}")
    
    exit(0)
