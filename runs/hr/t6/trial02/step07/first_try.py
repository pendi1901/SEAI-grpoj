import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement by using the acquire function
    from ezr, which is designed to optimize label usage (budget 50).
    """
    # Create a table structure. The rows provided have '?' in goal columns.
    # We need to label them to find the best one.
    tbl = ezr.Tbl([header] + rows)
    
    # The acquire function in ezr uses a budget (the.Stop) to label rows
    # and returns the rows that were labeled.
    # We need to map the labeled rows back to their original indices.
    
    # Create a mapping of row content to original index
    # We use a tuple of the row to make it hashable/comparable
    row_to_idx = {tuple(row): i for i, row in enumerate(rows)}
    
    # Perform the acquisition
    # label is the oracle provided by the harness
    labeled_rows = ezr.acquire(tbl, cap=50, label=label)
    
    # Find the best row among the labeled ones
    # Best is defined by ydist (lower is better)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    return row_to_idx[tuple(best_row)]

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
        
    # Define the oracle to reveal the true values
    def oracle(row):
        # Find the original row in the data
        # Since we need to return the full row, we look it up
        # In a real scenario, this would be a database lookup
        for original in rows:
            # Match on non-goal columns
            match = True
            for i in range(len(header)):
                if i not in goal_indices and original[i] != row[i]:
                    match = False
                    break
            if match:
                return original
        return row

    # Run the selection
    best_idx = choose(header, masked_rows, oracle)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at record index: {best_idx}")
    print(f"This record was identified using a budget of 50 interviews.")
    
    exit(0)
