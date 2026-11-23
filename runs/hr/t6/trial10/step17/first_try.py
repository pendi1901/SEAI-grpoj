import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff 
    within a budget of 50 labels.
    """
    # Filter rows for Laboratory Technician
    role_idx = header.index('jobRole')
    lab_rows = [r for r in rows if r[role_idx] == 'Laboratory Technician']
    
    # Map the filtered rows back to their original indices for the label function
    # We need to pass the original indices to the label function
    original_indices = [i for i, r in enumerate(rows) if r[role_idx] == 'Laboratory Technician']
    
    # Create a local label wrapper that maps the filtered index to the original index
    def lab_oracle(filtered_idx):
        original_idx = original_indices[filtered_idx]
        return label(original_idx)
    
    # Use the logic from step07 to find the best row among the filtered set
    # We pass the filtered rows and the wrapped oracle
    best_filtered_idx = step07.choose(header, lab_rows, lab_oracle)
    
    # Return the original index of the best row found
    return original_indices[best_filtered_idx]

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
