import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by using the acquire strategy to intelligently
    sample the search space within a budget of 50 labels.
    """
    # Create a table object for the data
    # We need to handle the fact that goals are currently "?"
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # The acquire function in ezr.py is designed to find the best rows
    # by balancing exploration and exploitation.
    # It takes a label function and a budget (the.Stop).
    # We set the budget to 50 as requested.
    ezr.the.Stop = 50
    
    # We need to map the rows back to their original indices.
    # Since acquire returns the rows themselves, we store them with their index.
    indexed_rows = []
    for i, row in enumerate(rows):
        indexed_rows.append((i, row))
    
    # We create a wrapper for the label function to track which original
    # row index is being labeled.
    labeled_data = []
    
    def oracle_wrapper(row):
        # Find the index of this row in the original list
        # We search for the row object reference
        for i, r in indexed_rows:
            if r is row:
                true_row = label(i)
                labeled_data.append((i, true_row))
                return true_row
        return row

    # Run the acquisition process
    # This will call label() up to 50 times
    ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among those we labeled
    # We use ydist to evaluate the quality of the labeled rows
    best_idx = -1
    best_dist = float('inf')
    
    for i, row in labeled_data:
        dist = ezr.ydist(tbl, row)
        if dist < best_dist:
            best_dist = dist
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # Create a local copy of rows with hidden goals for the simulation
    # The 'label' function will reveal the true values
    hidden_rows = []
    for row in all_rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name[-1] in "+-":
                new_row[i] = "?"
        hidden_rows.append(new_row)
        
    def label_func(i):
        return all_rows[i]
    
    best_index = choose(header, hidden_rows, label_func)
    
    print(f"Optimization complete.")
    print(f"The best configuration found is at index: {best_index}")
    print(f"Row data: {all_rows[best_index]}")
    
    exit(0)
