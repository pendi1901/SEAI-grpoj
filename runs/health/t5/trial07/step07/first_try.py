import ezr
import random

def choose(header, rows, label):
    """
    Find the best row among the provided rows using a budget of 50 labels.
    We use the acquire logic from ezr to sample the space effectively.
    """
    # Create a table object to manage column roles and distance metrics
    # We initialize with the header and a copy of the rows
    tbl = ezr.Tbl([header] + rows)
    
    # We need to track which rows we have already labeled to stay within budget
    # The acquire function in ezr takes an oracle. We wrap the provided label
    # function to ensure we only count unique calls.
    labeled_indices = {}
    
    def oracle_wrapper(row):
        # Find the original index of this row to track it
        # Since rows are passed by reference, we can find them in the original list
        idx = rows.index(row)
        if idx not in labeled_indices:
            labeled_indices[idx] = label(row)
        return labeled_indices[idx]

    # Use the acquire strategy to explore the space and find the best row
    # The acquire function returns a list of rows that have been labeled
    # and sorted by their ydist.
    best_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # The best row is the one with the lowest ydist (closest to ideal goals)
    # The acquire function sorts the best_rows by ydist, so the first one is best
    best_row = best_rows[0]
    
    # Return the index of the best row found
    return rows.index(best_row)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Create a copy of rows with goals masked as "?"
    # The customer's request implies we don't know the goals initially
    masked_rows = []
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the oracle to reveal the true values
    def label(row):
        # Find the original row in the dataset to return the true goals
        # This is a simple lookup since we have the full data
        idx = masked_rows.index(row)
        return rows[idx]
    
    # Run the selection process
    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete.")
    print(f"The best configuration found is at index {best_idx}.")
    print(f"Configuration details: {rows[best_idx]}")
