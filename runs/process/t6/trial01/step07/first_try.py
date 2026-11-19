import ezr
import step01

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use ezr.acquire to intelligently sample the space and find the best row.
    """
    # Create a table object from the provided rows
    # Note: The rows passed in have '?' for goals, but ezr.Tbl handles this.
    # We need to provide the header to define the columns.
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr.py is designed specifically for this task:
    # It takes a budget (the.Stop), a label function, and returns the best rows.
    # We set the budget to 50 as requested.
    # acquire returns the rows that were labeled.
    
    # We need to ensure the label function is used correctly.
    # The harness provides the label function.
    
    # We use the acquire logic to find the best rows.
    # Since acquire returns a list of rows, we find the one with the best ydist.
    labeled_rows = ezr.acquire(tbl, cap=50, label=label)
    
    # Find the best row among those labeled
    # We re-calculate ydist based on the now-labeled data
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row in the original rows list
    for i, row in enumerate(rows):
        if row == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Prepare rows with hidden goals
    test_rows = []
    for row in all_rows:
        new_row = row[:]
        new_row[9] = new_row[10] = new_row[11] = "?"
        test_rows.append(new_row)
        
    # Define the oracle to reveal goals
    def oracle(i):
        return all_rows[i]
    
    # Define the label function that the harness expects
    def label_wrapper(row):
        # Find index of row to return its true values
        for i, r in enumerate(test_rows):
            if r is row:
                return all_rows[i]
        return None
        
    best_idx = choose(header, test_rows, label_wrapper)
    
    print(f"Best configuration found at index: {best_idx}")
    print(f"Goal values: {all_rows[best_idx][9:]}")
    
    exit(0)
