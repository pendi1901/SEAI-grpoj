import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup for a large, high-stakes project.
    We use the acquire logic, which is designed to find the best rows
    with a minimal labeling budget (50).
    
    Fix: The previous error occurred because the oracle_wrapper was trying to 
    modify the row in-place using indices that didn't match the true_row 
    structure or by attempting to update the row object incorrectly.
    We now use a simple dictionary to track labeled rows and return the index.
    """
    # Create a table structure to manage the data
    tbl = ezr.Tbl([header] + rows)
    
    # Track labeled rows
    labeled_indices = {}

    def oracle_wrapper(row):
        # Find the index of this row in the original list
        # We search for the row by comparing values
        for i, r in enumerate(rows):
            if r == row:
                idx = i
                break
        
        # Get the true values
        true_row = label(idx)
        
        # Update the row in-place to ensure ezr's internal logic sees the values
        for i in range(len(row)):
            row[i] = true_row[i]
            
        labeled_indices[idx] = row
        return row

    # Use the acquire function to pick and label up to 50 rows
    ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among the labeled ones.
    # A row is better if its ydist is lower.
    best_idx = min(labeled_indices.keys(), key=lambda i: ezr.ydist(tbl, labeled_indices[i]))
    
    return best_idx

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the choose function
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
    
    # Define the label function for the harness
    def label_func(idx):
        return rows[idx]
    
    # Find the best setup
    best_idx = choose(header, masked_rows, label_func)
    
    # Calculate the actual performance of the chosen row
    tbl = ezr.Tbl(data)
    dist = ezr.ydist(tbl, rows[best_idx])
    
    print("Analysis: Finding the best setup for a high-stakes, large project.")
    print(f"Best setup found at index: {best_idx}")
    print(f"Performance (ydist to ideal): {dist:.4f}")
    print("This setup was identified using a minimal labeling budget of 50 samples.")
    exit(0)
