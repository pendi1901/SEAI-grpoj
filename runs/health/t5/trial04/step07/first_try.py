import ezr
import random

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use the acquire function from ezr, which implements a 
    multi-objective search strategy to find the best rows 
    within a limited labeling budget.
    """
    # Create a table object to manage the data
    # We use a copy of rows because acquire might modify them
    tbl = ezr.Tbl([header] + [list(r) for r in rows])
    
    # The acquire function performs the search.
    # It takes the table, the budget (50), and the oracle (label).
    # It returns the rows that were labeled and evaluated.
    # We wrap the label function to map the index back to the row.
    def oracle_wrapper(row):
        # Find the index of this row in the original list to call label()
        # Note: This assumes rows are unique or we just need the label for the content
        for i, r in enumerate(rows):
            if r == row:
                return label(i)
        return row

    # Perform the acquisition
    # ezr.acquire returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones
    # A row is better if its ydist is lower (closer to 0)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    for i, r in enumerate(rows):
        if r == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Setup for the test harness
    # The label function reveals the hidden goal values
    def label(i):
        return all_data[i+1]

    # Mask the goals in the rows provided to the function
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Run the selection
    best_idx = choose(header, masked_rows, label)
    
    # Print results
    best_row = all_data[best_idx + 1]
    print(f"Search complete. Best configuration found at index {best_idx}.")
    print(f"Performance metrics for this setup:")
    for i in goal_indices:
        print(f" - {header[i]}: {best_row[i]:.4f}")
    
    exit(0)
