import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement using at most 50 labels.
    We use the 'acquire' strategy from ezr to intelligently select
    rows to label, then return the index of the best one found.
    """
    # Create a table object to manage the data
    # We need to handle the fact that rows have '?' for goals
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr.py performs active learning.
    # It takes a budget (the.Stop) and an oracle (label function).
    # We need to map the label function to the row indices.
    
    # Create a wrapper for the label function that works with indices
    # and updates the rows in place.
    def oracle_wrapper(row):
        # Find the original index of this row
        # Since rows are passed by reference, we can find the index
        idx = rows.index(row)
        true_row = label(idx)
        # Update the row with the true values
        for i, val in enumerate(true_row):
            row[i] = val
        return row

    # Use ezr.acquire to select and label rows
    # ezr.acquire returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among those labeled
    # A row is better when its ydist is lower
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    # Load the data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Keep a copy of the original rows to provide to the label function
    # The rows passed to choose() will have goals masked as '?'
    full_data = [list(r) for r in rows]
    
    # Mask the goals in the rows provided to the choose function
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in full_data:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function
    def label(i):
        return full_data[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label)
    
    # Print the result
    print(f"Best employee arrangement found at index: {best_idx}")
    print("Goal values for this employee:")
    for idx in goal_indices:
        print(f"  {header[idx]}: {full_data[best_idx][idx]}")
    
    exit(0)
