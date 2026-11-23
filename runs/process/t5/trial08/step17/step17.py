import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup for a large, high-stakes project.
    We use the 'acquire' strategy which is designed to find the best rows
    within a limited label budget (50).
    """
    # Create a table object from the provided data
    tbl = ezr.Tbl([header] + rows)
    
    # We need to ensure the label function updates the row's goal cells
    # so that the acquisition logic can evaluate them correctly.
    def oracle_wrapper(row):
        # Find the index of this row in the original list
        idx = rows.index(row)
        true_vals = label(idx)
        # Update the row with the true goal values
        goal_indices = [c.at for c in tbl.y]
        for i, g_idx in enumerate(goal_indices):
            row[g_idx] = true_vals[i]
        return row

    # Run the acquisition process:
    # This intelligently samples the space to find the best configuration
    # while respecting the 50-label budget.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones.
    # Lower ydist is better (closer to ideal goals).
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
    
    print(f"Optimization complete for high-stakes project.")
    print(f"Best configuration found at index: {best_idx}")
    print(f"Total labels used: {len(labeled_indices)}")
    print("This configuration minimizes risk and maximizes performance based on our analysis.")
    
    exit(0)
