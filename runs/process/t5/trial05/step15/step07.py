import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by using the acquire strategy to explore the space
    within a budget of 50 labels.
    """
    # Create a table object. 
    # We must ensure the table is initialized with rows that have numeric values
    # where possible, but since we are given rows with '?', we must handle
    # the fact that ezr.Tbl will see '?' as a string.
    # We will use a subset of rows to initialize the table's column statistics
    # or simply use the provided rows and handle the '?' in the label function.
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Track labeled rows
    labeled_data = []

    def tracked_label(row):
        # Find the index of the row in the original list
        # We use the row object identity to find the index
        idx = -1
        for i, r in enumerate(rows):
            if r is row:
                idx = i
                break
        
        # Get the true values from the oracle
        true_vals = label(idx)
        
        # Update the row in place
        for i, val in enumerate(true_vals):
            row[i] = val
            
        # Update the table's column statistics with the new information
        ezr.addCols(tbl, row, 1)
        
        labeled_data.append((idx, row))
        return row

    # Use the acquire logic to explore the space.
    # We limit the budget to 50.
    ezr.acquire(tbl, cap=50, label=tracked_label)
    
    # Find the best row among those we labeled
    best_idx = -1
    best_ydist = float('inf')
    
    for idx, row in labeled_data:
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
