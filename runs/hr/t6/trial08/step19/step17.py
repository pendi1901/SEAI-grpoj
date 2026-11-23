import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best laboratory staff arrangement using a limited label budget.
    Filters the dataset for 'Laboratory Technician' role before running the
    selection process.
    """
    # Identify the jobRole column index
    role_idx = header.index("jobRole")
    
    # Filter rows for Laboratory Technicians
    lab_rows = [r for r in rows if r[role_idx] == "Laboratory Technician"]
    
    # We need to map the filtered rows back to their original indices
    # to use the provided label(i) function correctly.
    original_indices = [i for i, r in enumerate(rows) if r[role_idx] == "Laboratory Technician"]
    
    # Create a mapping for the oracle.
    # The oracle in step07 expects an index and returns the full row.
    # We define a wrapper that maps the index back to the original dataset.
    def lab_label(i):
        # i is the index in the original dataset
        return label(i)

    # We need to perform the selection on the lab_rows.
    # To avoid the IndexError in step07's oracle_wrapper, we must ensure
    # the table structure matches the rows provided.
    
    # Create a table object with the lab_rows
    indexed_lab_rows = [list(r) + [original_indices[i]] for i, r in enumerate(lab_rows)]
    new_header = header + ["idxX"]
    tbl = ezr.Tbl([new_header] + indexed_lab_rows)
    
    # Define an oracle that calls the provided label function using the stored index
    def oracle_wrapper(row):
        idx = int(row[-1])
        full_row = label(idx)
        # Update the row with real values from the full_row
        for i, name in enumerate(header):
            if name.endswith('+') or name.endswith('-'):
                row[i] = full_row[i]
        return row

    # Use ezr.acquire to spend the 50-label budget.
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones.
    # A row is better when its ydist is lower.
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    return int(best_row[-1])

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals for the input
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name.endswith('+') or name.endswith('-'):
                new_row[i] = "?"
        masked_rows.append(new_row)
    
    # Define the real label function
    def real_label(i):
        return rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, real_label)
    
    print("Laboratory Staff Retention Analysis")
    print("-" * 50)
    print(f"Best laboratory staff arrangement found at index: {best_idx}")
    
    # Extract goal values for display
    goal_vals = [rows[best_idx][i] for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    print(f"Goal values for this employee: {goal_vals}")
    print("-" * 50)
    print("This selection was optimized using a limited label budget.")
