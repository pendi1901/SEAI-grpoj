import ezr
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    using the acquire function with a budget of 50 labels.
    """
    # Filter rows for Laboratory Technician
    job_idx = header.index("jobRole")
    lab_rows = [r for r in rows if r[job_idx] == "Laboratory Technician"]
    
    # If no lab staff found, return 0
    if not lab_rows:
        return 0
        
    # We need to map the filtered rows back to their original indices
    # to satisfy the label(i) requirement.
    original_indices = [i for i, r in enumerate(rows) if r[job_idx] == "Laboratory Technician"]
    
    # Create a table for the filtered subset
    tbl = ezr.Tbl([header] + lab_rows)
    
    # Oracle wrapper to map the filtered row back to the original index
    def oracle_wrapper(row):
        # Find the original index of this row
        for i, original_row in enumerate(lab_rows):
            if all(row[j] == "?" or row[j] == original_row[j] for j in range(len(header))):
                return label(original_indices[i])
        return row

    # Perform the acquisition on the filtered table
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Find the best row among the labeled ones (lowest ydist)
    best_row = min(labeled_rows, key=lambda r: ezr.ydist(tbl, r))
    
    # Return the original index of the best row
    for i, row in enumerate(lab_rows):
        if row == best_row:
            return original_indices[i]
    return original_indices[0]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the oracle
    def oracle(i):
        return rows[i]

    best_idx = choose(header, masked_rows, oracle)
    
    print(f"Analysis complete for Laboratory Technician staff.")
    print(f"The best working arrangement found is at record index: {best_idx}")
    print(f"This was identified using a budget of 50 interviews.")
    
    exit(0)
