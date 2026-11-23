import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff 
    by sampling up to 50 rows, labeling them, and picking the best.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    role_idx = header.index('jobRole')
    
    # Filter indices for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[role_idx] == 'Laboratory Technician']
    
    if not lab_indices:
        return 0
    
    # We want to maximize columns ending in '+' and minimize columns ending in '-'
    def score_row(goals):
        score = 0
        for i, val in enumerate(goals):
            name = header[goal_indices[i]]
            if name.endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Sample up to 50 indices from the lab staff
    sample_indices = random.sample(lab_indices, min(50, len(lab_indices)))
    
    best_idx = -1
    best_score = float('-inf')
    
    for idx in sample_indices:
        true_goals = label(idx)
        current_score = score_row(true_goals)
        
        if current_score > best_score:
            best_score = current_score
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Create a local label function for the harness
    def label(i):
        return [rows[i][idx] for idx in goal_indices]

    # Mask the goal columns
    for row in rows:
        for idx in goal_indices:
            row[idx] = '?'

    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete. The best working arrangement for Laboratory Technicians is at index {best_idx}.")
    print("This selection was determined by sampling up to 50 laboratory staff members and evaluating their goal metrics.")
