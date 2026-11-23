import csv
import random

def choose(header, rows, label):
    """
    Finds the best row for 'Laboratory Technician' staff by sampling 
    up to 50 rows, labeling them, and returning the index of the row 
    with the highest 'YearsAtCompany+' value.
    """
    # Identify goal column (first one ending in +)
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    role_idx = header.index('jobRole')
    
    # Filter for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # If no lab staff found, return any valid index
    if not lab_indices:
        return 0
    
    # Budget of 50 labels
    sample_size = min(50, len(lab_indices))
    indices_to_sample = random.sample(lab_indices, sample_size)
    
    best_idx = -1
    best_val = -float('inf')
    
    for i in indices_to_sample:
        # label(i) returns the true goal values
        goals = label(i)
        val = goals[0]
        
        if val > best_val:
            best_val = val
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Define label function for the harness
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    
    def label(i):
        return [rows[i][goal_idx]]
    
    # Run the selection
    best_index = choose(header, rows, label)
    
    print("Laboratory Staff Retention Analysis:")
    print(f"The best arrangement for a Laboratory Technician was found at index {best_index}.")
    print(f"YearsAtCompany+ for this employee: {rows[best_index][goal_idx]}")
    print("Logic: Sampled Laboratory Technician roles to identify the longest-tenured employee.")
