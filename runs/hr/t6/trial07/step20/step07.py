import ezr

def choose(header, rows, label):
    """
    Uses the acquire function from ezr to select the best working arrangement
    within a budget of 50 labels.
    """
    # Create a table object from the provided rows.
    # Note: The rows passed to choose have '?' in goal columns.
    tbl = ezr.Tbl([header] + rows)
    
    # Map rows to their original indices to return the correct index later.
    # We use id() to handle potential duplicate row content.
    row_to_idx = {id(r): i for i, r in enumerate(rows)}
    
    # Identify goal column indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    
    def oracle(row):
        # Find the index of this row
        idx = row_to_idx[id(row)]
        # Get true goals from the harness
        true_goals = label(idx)
        # Update the row with the true goal values
        for i, goal_val in zip(goal_indices, true_goals):
            row[i] = goal_val
        return row

    # Use ezr.acquire to spend the budget of 50 labels.
    # ezr.acquire returns the rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Find the best row among the ones we labeled.
    # Lower ydist is better.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the index of the best row found
    return row_to_idx[id(best_row)]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Prepare rows with masked goals
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    masked_rows = []
    for row in all_rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label(i):
        return [all_rows[i][idx] for idx in goal_indices]
    
    best_idx = choose(header, masked_rows, label)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at row index {best_idx}.")
    print(f"Details: {all_rows[best_idx]}")
