import ezr
import random

def choose(header, rows, label):
    """
    Find the best setup by using the acquire logic from ezr.
    We have a budget of 50 labels.
    """
    # Create a table structure to handle column roles and distance calculations
    # We initialize with the header and empty rows, then add rows as we label them
    tbl = ezr.Tbl([header])
    
    # We need to keep track of which rows we have already labeled
    # to ensure we don't exceed the 50-row budget.
    labeled_indices = {}
    
    def oracle_wrapper(row):
        # Find the index of this row in the original list to call the provided label()
        # Since rows are passed by reference, we can find the index
        for i, r in enumerate(rows):
            if r is row:
                if i not in labeled_indices:
                    labeled_indices[i] = label(row)
                return labeled_indices[i]
        return row

    # Use ezr.acquire to spend the budget of 50 labels.
    # The acquire function returns the rows that were labeled.
    # We pass the full dataset as the table to allow the acquisition logic
    # to sample from the entire space.
    full_tbl = ezr.Tbl([header] + rows)
    
    # acquire() uses the.Stop (default 50) as the budget.
    labeled_rows = ezr.acquire(full_tbl, cap=50, label=oracle_wrapper)
    
    # After labeling, find the best row among the ones we labeled.
    # A row is better when its ydist is lower.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(full_tbl, r))
    
    # Return the index of the best row found
    for i, r in enumerate(rows):
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Mask the goals for the choose function
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function that reveals the true goals
    def label(row):
        # Find original row to get true values
        for i, r in enumerate(masked_rows):
            if r is row:
                return rows[i]
        return row

    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete. Best setup found at index {best_idx} (1-based: {best_idx + 1}).")
    exit(0)
