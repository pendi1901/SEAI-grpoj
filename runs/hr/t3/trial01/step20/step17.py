import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff.
    We sample up to 50 rows that match this job role and pick the one
    with the highest 'YearsAtCompany+' (a '+' goal).
    """
    job_role_idx = header.index('jobRole')
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_indices[0]  # YearsAtCompany+
    
    # Filter indices for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[job_role_idx] == 'Laboratory Technician']
    
    # Sample up to 50
    sample_size = min(len(lab_indices), 50)
    indices_to_query = random.sample(lab_indices, sample_size)
    
    best_idx = -1
    best_val = -float('inf')
    
    for idx in indices_to_query:
        # Get true values for this row
        true_goals = label(idx)
        val = true_goals[0] # YearsAtCompany+
        
        # Since it's a '+' goal, higher is better
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
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Store true goal values to simulate the label function
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    true_data = [[row[i] for i in goal_indices] for row in rows]
    
    # Mask rows
    for row in rows:
        for i in goal_indices:
            row[i] = "?"
            
    def label(i):
        return true_data[i]
        
    best_idx = choose(header, rows, label)
    
    if best_idx != -1:
        print(f"Analysis complete for Laboratory Technicians.")
        print(f"The best working arrangement found is at row index: {best_idx}")
        print(f"This employee has been with the company for {true_data[best_idx][0]} years.")
        print("Logic: Sampled up to 50 Laboratory Technicians and selected the one with the highest 'YearsAtCompany+' value.")
    else:
        print("No Laboratory Technicians found in the dataset.")
