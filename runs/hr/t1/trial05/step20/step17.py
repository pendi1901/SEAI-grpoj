import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff
    by sampling up to 50 rows, labeling them, and picking the one with 
    the highest composite score.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    idx_role = header.index('jobRole')
    
    # Filter for Laboratory Technician staff
    lab_indices = [i for i, row in enumerate(rows) if row[idx_role] == 'Laboratory Technician']
    
    def get_score(goals):
        score = 0
        for i, g_idx in enumerate(goal_indices):
            val = goals[i]
            # + goals: maximize, - goals: minimize
            if header[g_idx].endswith('+'):
                score += val
            else:
                score -= val
        return score

    # Sample up to 50 indices from the lab staff
    num_to_sample = min(50, len(lab_indices))
    indices_to_label = random.sample(lab_indices, num_to_sample)
    
    best_idx = -1
    best_score = float('-inf')
    
    for idx in indices_to_label:
        true_goals = label(idx)
        score = get_score(true_goals)
        
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Store true goals for the label function
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    true_data = {i: [rows[i][g] for g in goal_indices] for i in range(len(rows))}
    
    # Mask rows
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    def label(i):
        return true_data[i]

    best_idx = choose(header, rows, label)
    
    print("Optimization Result for Laboratory Staff:")
    print(f"The best working arrangement found is at row index: {best_idx}")
    print("This selection was determined by sampling up to 50 Laboratory Technicians")
    print("and identifying the one with the highest tenure-based performance score.")
