import csv
import random
import step07

def choose(header, rows, label):
    """
    Finds the best row for 'Laboratory Technician' staff by sampling 
    up to 50 rows, labeling them, and returning the index of the 
    one with the highest 'YearsAtCompany+'.
    """
    # Identify the goal column
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+'):
            goal_idx = i
            break
            
    # Identify the jobRole column
    role_idx = header.index('jobRole')
    
    # Filter indices for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # Sample up to 50 indices from the lab staff
    sample_size = min(50, len(lab_indices))
    sample_indices = random.sample(lab_indices, sample_size)
    
    best_idx = -1
    best_val = -float('inf')
    
    for idx in sample_indices:
        # label(i) returns the true goal values for rows[i]
        true_goals = label(idx)
        val = true_goals[0] # YearsAtCompany+
        
        if val > best_val:
            best_val = val
            best_idx = idx
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
        
        for row in reader:
            new_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        new_row.append(float(val))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(val)
            rows.append(new_row)
            
    def label(i):
        return [rows[i][g] for g in goal_indices]
    
    # Mask the goal columns for the choose function
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for g in goal_indices:
            new_row[g] = "?"
        masked_rows.append(new_row)
        
    best_idx = choose(header, masked_rows, label)
    
    if best_idx != -1:
        print(f"Analysis complete. After interviewing laboratory staff, the best working arrangement "
              f"was found at row {best_idx}.")
        print(f"This employee has a tenure of {rows[best_idx][goal_indices[0]]} years.")
    else:
        print("No laboratory staff found to evaluate.")
