import ezr
import random

def choose(header, rows, label):
    """
    Find the best row using a budget of 50 labels.
    We use the 'acquire' strategy from ezr to intelligently sample 
    the search space, then return the index of the best row found.
    """
    # Create a table object to manage the data
    # We need to handle the fact that goal cells are '?'
    # We will use the provided label function to reveal them.
    
    # We need to track the original indices because we are returning an index
    indexed_rows = []
    for i, row in enumerate(rows):
        indexed_rows.append((i, row))
        
    # The acquire function in ezr expects a TBL object.
    # We create a TBL from the rows that have goals (if any) or just the structure.
    # Since the prompt says all goal cells are '?', we must use the label function.
    
    # We will use a subset of the data to build our initial model
    # and then use the acquire logic to pick the best.
    
    # To satisfy the 50 label limit:
    # 1. Use the provided label function to reveal goals for selected rows.
    # 2. Use ezr.acquire to intelligently pick which rows to label.
    
    # We create a wrapper for the label function to track indices
    labeled_data = []
    
    def oracle_wrapper(row):
        # Find the original index of this row
        # Since rows are passed by reference, we can find it in our indexed list
        for i, r in indexed_rows:
            if r is row:
                revealed = label(i)
                # Update the row in place with the revealed values
                for j, val in enumerate(revealed):
                    row[j] = val
                labeled_data.append(row)
                return row
        return row

    # Build a TBL structure
    tbl = ezr.Tbl([header] + rows)
    
    # Use ezr's acquire logic to find the best rows within the budget
    # ezr.acquire uses the.Stop (default 50) as the budget
    best_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the ones we labeled
    best_row = min(best_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row
    for i, r in indexed_rows:
        if r is best_row:
            return i
    return 0

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals as per requirements
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    # Define the label function
    # In this context, we have the full data, so we just return the original values
    full_data = list(ezr.csv(filename))
    full_rows = full_data[1:]
    
    def label(i):
        return [full_rows[i][idx] for idx in goal_indices]
    
    # Run the choice
    best_idx = choose(header, rows, label)
    
    print(f"Optimization complete.")
    print(f"The best setup found is at index: {best_idx}")
    print(f"Goal values for this setup: {label(best_idx)}")
    
    exit(0)
