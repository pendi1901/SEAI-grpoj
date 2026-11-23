import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best arrangement for 'Laboratory Technician' staff only,
    using the active learning search within a 50-label budget.
    """
    # Filter rows for Laboratory Technician
    idx_role = header.index("jobRole")
    lab_indices = [i for i, r in enumerate(rows) if r[idx_role] == "Laboratory Technician"]
    
    # If no lab staff, return first row
    if not lab_indices:
        return 0
    
    # Create a mapping from local index to global index
    # The harness expects us to return the index in the original 'rows' list
    # We create a subset for the search
    lab_rows = [rows[i] for i in lab_indices]
    
    # We need a wrapper for the label function to map back to global indices
    def lab_label(i):
        # i is the index in the lab_rows list
        global_idx = lab_indices[i]
        return label(global_idx)
    
    # Use the logic from step07 to perform the search
    # We pass the lab_rows (which have goals masked as "?")
    best_local_idx = step07.choose(header, lab_rows, lab_label)
    
    # Return the global index
    return lab_indices[best_local_idx]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goal columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label_func(i):
        return rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Best laboratory staff arrangement found at index: {best_idx}")
    print("This row represents the optimal balance of goals for laboratory staff "
          "based on targeted interviews.")
