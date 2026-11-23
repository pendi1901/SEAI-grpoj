import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement for 'Laboratory Technician' staff 
    using a budget of 50 labels.
    """
    # Identify the index for 'jobRole'
    job_role_idx = header.index("jobRole")
    
    # Filter rows to only include 'Laboratory Technician'
    # We keep track of the original indices to return the correct one
    lab_rows_with_indices = [
        (i, row) for i, row in enumerate(rows) 
        if row[job_role_idx] == "Laboratory Technician"
    ]
    
    if not lab_rows_with_indices:
        return 0
    
    # Extract just the rows for the table
    lab_rows = [r for i, r in lab_rows_with_indices]
    
    # Create a table object for the laboratory staff
    tbl = ezr.Tbl([header] + lab_rows)
    
    # Map internal table row index to original dataset index
    # The oracle must return the full row (including goals)
    def oracle(row):
        # Find the original index of this row
        for i, r in lab_rows_with_indices:
            if r is row:
                true_row = label(i)
                # Update the row in place with the true values
                # We update the row object directly
                for j in range(len(row)):
                    row[j] = true_row[j]
                return row
        return row

    # Use ezr.acquire to spend the budget on the laboratory staff subset
    # Note: acquire returns the rows that were labeled.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle)
    
    # Find the best row among the ones we labeled
    # A row is better if its ydist is lower (closer to 0).
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index of the best row found
    for i, r in lab_rows_with_indices:
        if r is best_row:
            return i
            
    return lab_rows_with_indices[0][0]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goal columns for the input to choose()
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # The harness provides the true data
    def label_func(idx):
        return rows[idx]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis complete for Laboratory Technician staff.")
    print(f"The best working arrangement found is at record index: {best_idx}")
    print(f"This record has been identified as having the most favorable outcomes "
          f"for laboratory staff based on the 50-label budget.")
    
    exit(0)
