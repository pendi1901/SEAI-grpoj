import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, 
    labeling them to find their true goal values, and picking the best.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
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

    # Randomly sample 50 indices to label
    indices = list(range(len(rows)))
    sample_indices = random.sample(indices, min(50, len(rows)))
    
    best_idx = -1
    best_score = float('-inf')
    
    for idx in sample_indices:
        # Get true values for the goals
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
    
    print(f"Analysis complete. The best working arrangement found is at index {best_idx}.")
    print("This selection was determined by sampling 50 staff members and evaluating their goal metrics.")
