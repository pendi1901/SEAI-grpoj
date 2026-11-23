import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff 
    within a budget of 50 labels.
    """
    # Filter rows for Laboratory Technician
    role_idx = header.index('jobRole')
    
    # We need to keep track of the original indices to return the correct one
    # and to call the label function correctly.
    lab_indices = [i for i, r in enumerate(rows) if r[role_idx] == 'Laboratory Technician']
    lab_rows = [rows[i] for i in lab_indices]
    
    # The harness expects us to label rows[i]. 
    # step07.choose expects a label function that takes an index 
    # relative to the list passed to it.
    def lab_oracle(filtered_idx):
        original_idx = lab_indices[filtered_idx]
        return label(original_idx)
    
    # We cannot use step07.choose directly because it expects to build a Tbl 
    # from the rows passed to it, but the rows passed to it might have '?' 
    # in goal columns, which ezr.Tbl handles fine, but the oracle must 
    # return the full row.
    
    # Re-implementing the selection logic to ensure we handle the Tbl correctly
    tbl = ezr.Tbl([header] + lab_rows)
    
    # We need to ensure the oracle returns the full row (with goals filled)
    # when called by acquire.
    def oracle_wrapper(row):
        # Find which index in lab_rows this row corresponds to
        # Since rows are objects, we can find the index in lab_rows
        idx = lab_rows.index(row)
        return lab_oracle(idx)
        
    best_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Sort the labeled rows by ydist (lower is better)
    best_rows.sort(key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index of the best row found
    best_row = best_rows[0]
    return lab_indices[lab_rows.index(best_row)]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Create masked rows for the simulation
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for i, name in enumerate(header):
            if name.endswith("+") or name.endswith("-"):
                new_row[i] = "?"
        masked_rows.append(new_row)
        
    # Define the label function for the harness
    def label_func(i):
        return rows[i]
    
    # Run the selection
    best_idx = choose(header, masked_rows, label_func)
    
    print("Analysis: Best working arrangement for Laboratory Technicians.")
    print(f"The best arrangement found is at index {best_idx}.")
    print("Logic: Filtered for 'Laboratory Technician' role and used model-based acquisition.")
