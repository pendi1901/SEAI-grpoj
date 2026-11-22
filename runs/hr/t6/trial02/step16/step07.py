import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement by using the acquire function
    from ezr, which is designed to optimize label usage (budget 50).
    """
    # Create a table structure.
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr uses a budget (the.Stop) to label rows.
    # To handle the oracle, we wrap the provided label function to ensure
    # we return the full row (with goals) to the table.
    def oracle_wrapper(row):
        # The harness expects us to call label(i) where i is the index.
        # We need to find the index of the row passed to us.
        # Since we cannot hash lists, we find the index by reference/content.
        for i, original_row in enumerate(rows):
            if all(row[j] == "?" or row[j] == original_row[j] for j in range(len(header))):
                return label(i)
        return row

    # Perform the acquisition
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones.
    # Best is defined by ydist (lower is better).
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    for i, row in enumerate(rows):
        if row == best_row:
            return i
    return 0

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the choose function
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the oracle to reveal the true values for the harness
    def oracle(i):
        return rows[i]

    # Run the selection
    best_idx = choose(header, masked_rows, oracle)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at record index: {best_idx}")
    print(f"This record was identified using a budget of 50 interviews.")
    
    exit(0)
