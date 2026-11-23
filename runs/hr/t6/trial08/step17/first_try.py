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
    
    # Create a mapping for the oracle
    def lab_label(i):
        # i here is the index in the lab_rows list
        original_idx = original_indices[i]
        return label(original_idx)

    # Use the selection logic from step07, but restricted to lab_rows
    # We pass the lab_rows and a wrapper that handles the index mapping
    best_lab_idx = step07.choose(header, lab_rows, lab_label)
    
    # Return the original index of the best row found
    return original_indices[best_lab_idx]

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
