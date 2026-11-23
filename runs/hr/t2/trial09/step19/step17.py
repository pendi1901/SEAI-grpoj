import csv
import random
import step07

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    by sampling up to 50 rows from that specific job role.
    """
    role_idx = header.index('jobRole')
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    # We can label at most 50 rows.
    sample_size = min(50, len(lab_indices))
    sampled_indices = random.sample(lab_indices, sample_size)
    
    best_idx = -1
    best_score = -float('inf')
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    for idx in sampled_indices:
        # Get true values for the goals
        true_goals = label(idx)
        
        # Create a temporary row with true values to calculate score
        temp_row = list(rows[idx])
        for i, g_idx in enumerate(goal_indices):
            temp_row[g_idx] = true_goals[i]
            
        score = step07.get_score(header, temp_row)
        
        if score > best_score:
            best_score = score
            best_idx = idx
            
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label(i):
        return [rows[i][g] for g in goal_indices]
    
    # Mask the rows as per instructions
    for row in rows:
        for g in goal_indices:
            row[g] = "?"
            
    best_row_idx = choose(header, rows, label)
    
    print("Analysis complete.")
    print(f"The best working arrangement found for Laboratory Technicians is at row index: {best_row_idx}")
    print("This selection was based on an in-depth evaluation of sampled laboratory staff.")
