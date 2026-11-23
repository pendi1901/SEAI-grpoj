import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by using the acquire strategy to explore the space
    within a budget of 50 labels.
    """
    # Create a table object. The rows currently have '?' for goals.
    # We need to label them to understand the landscape.
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # The acquire function in ezr.py is designed to find the best rows
    # using a limited label budget. It returns the rows that were labeled.
    # We set the budget to 50 as requested.
    
    # We need to wrap the label function to track which rows we've labeled
    # and return the index of the best one found.
    labeled_rows = []
    
    def tracked_label(row):
        # Find the original index of this row
        # Since rows are passed by reference, we can find the index
        idx = rows.index(row)
        true_row = label(idx)
        # Update the row in our local list with the true values
        for i, val in enumerate(true_row):
            row[i] = val
        labeled_rows.append((idx, row))
        return row

    # Use the acquire logic to explore the space
    # ezr.acquire uses the.Stop (default 50) as the budget
    ezr.acquire(tbl, cap=50, label=tracked_label)
    
    # Now find the best row among those we labeled
    # A row is better if its ydist is lower
    best_idx = -1
    best_ydist = float('inf')
    
    for idx, row in labeled_rows:
        current_ydist = ezr.ydist(tbl, row)
        if current_ydist < best_ydist:
            best_ydist = current_ydist
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    all_rows = list(rows_gen)
    
    # Keep a copy of the original rows to provide to the label function
    # Mask the goals for the input to the choose function
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    
    # Create a copy of rows with goals masked
    masked_rows = []
    for r in all_rows:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function
    def label_func(i):
        return all_rows[i]
    
    # Run the selection
    best_index = choose(header, masked_rows, label_func)
    
    print(f"Optimization complete. Best row found at index: {best_index}")
    print(f"Row details: {all_rows[best_index]}")
