import csv
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff 
    by sampling up to 50 rows, prioritizing those in the target role.
    """
    # Identify goal column and role column
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    role_idx = header.index('jobRole')
    
    # Filter indices for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # If we have fewer than 50, we label all of them. 
    # If more, we sample 50.
    if len(lab_indices) > 50:
        import random
        sample_indices = random.sample(lab_indices, 50)
    else:
        sample_indices = lab_indices
        
    best_idx = -1
    best_val = -float('inf')
    
    # Evaluate the sampled rows
    for i in sample_indices:
        # label(i) returns the true goal values
        true_goals = label(i)
        val = true_goals[0]
        
        if val > best_val:
            best_val = val
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
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

    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # The harness expects us to use the label function provided
    labeled_data = {}
    def label(i):
        if i not in labeled_data:
            labeled_data[i] = [rows[i][goal_idx]]
        return labeled_data[i]

    best_row_idx = choose(header, rows, label)
    
    if best_row_idx != -1:
        print(f"Analysis complete for Laboratory Technicians.")
        print(f"Best row found at index {best_row_idx}.")
        print(f"Value for '{header[goal_idx]}': {rows[best_row_idx][goal_idx]}")
    else:
        print("No Laboratory Technician staff found to analyze.")
