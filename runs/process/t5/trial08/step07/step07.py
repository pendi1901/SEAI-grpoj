import ezr
import random

def choose(header, rows, label):
    """
    Find the best row by using a budget of 50 labels.
    We use the 'acquire' strategy from ezr to intelligently sample
    the search space and identify the best configuration.
    """
    # Create a table object from the provided data
    # We need to ensure the table knows about the columns
    tbl = ezr.Tbl([header] + rows)
    
    # The 'acquire' function in ezr is designed to find the best rows
    # within a given label budget. It uses a combination of random
    # sampling and distance-based exploration to find high-performing
    # configurations.
    
    # We define a wrapper for the label function to handle the row indices
    # as expected by the ezr.acquire logic.
    def oracle_wrapper(row):
        # Find the index of this row in the original list
        # Note: This assumes rows are unique or we are okay with the first match
        idx = rows.index(row)
        true_vals = label(idx)
        # Update the row with the true goal values
        goal_indices = [c.at for c in tbl.y]
        for i, g_idx in enumerate(goal_indices):
            row[g_idx] = true_vals[i]
        return row

    # Run the acquisition process
    # ezr.acquire returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    # Lower ydist is better
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    return rows.index(best_row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty or missing.")
        exit(1)
        
    # Keep track of labeled indices to enforce the 50-label limit
    labeled_indices = set()
    
    def label_func(idx):
        if idx not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise Exception("Label budget exceeded!")
            labeled_indices.add(idx)
        # Return the original row's goal values
        # In this simulation, we know the full data
        return [rows[idx][c.at] for c in ezr.Tbl([header] + rows).y]

    # Mask the goals in the rows for the choose function
    goal_indices = [i for i, name in enumerate(header) if name[-1] in ('-', '+')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Optimization complete.")
    print(f"Best configuration found at index: {best_idx}")
    print(f"Total labels used: {len(labeled_indices)}")
    
    exit(0)
