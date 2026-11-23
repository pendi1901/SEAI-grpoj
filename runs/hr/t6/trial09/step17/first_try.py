import ezr
import step07

def choose(header, rows, label):
    """
    Find the best working arrangement for 'Laboratory Technician' staff
    using a budget of 50 labels.
    """
    # Identify the jobRole index
    job_idx = header.index('jobRole')
    
    # Filter rows for Laboratory Technician
    lab_tech_indices = [i for i, r in enumerate(rows) if r[job_idx] == 'Laboratory Technician']
    lab_tech_rows = [rows[i] for i in lab_tech_indices]
    
    # We need to map the local index back to the original index for the label() function
    # Create a wrapper for the label function
    def lab_oracle(i):
        # i is the index in lab_tech_rows, map to original index
        return label(lab_tech_indices[i])
    
    # Use the logic from step07 to perform the acquisition
    # We pass the filtered rows and the wrapped oracle
    return lab_tech_indices[step07.choose(header, lab_tech_rows, lab_oracle)]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Mask the goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_rows.append(new_row)
        
    # Define the oracle for the harness
    labeled_indices = set()
    
    def label_harness(i):
        if i not in labeled_indices:
            if len(labeled_indices) >= 50:
                raise Exception("Budget exceeded")
            labeled_indices.add(i)
        return rows[i]

    # Run the selection
    best_idx = choose(header, masked_rows, label_harness)
    
    print(f"Analysis complete. Best working arrangement for Laboratory Technicians found at index {best_idx}.")
    print(f"This arrangement has 'YearsAtCompany+': {rows[best_idx][31]}")
    print(f"This arrangement has 'YearsInCurrentRole+': {rows[best_idx][32]}")
    
    exit(0)
