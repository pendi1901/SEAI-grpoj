import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, 
    labeling them to get their true goal values, and picking the 
    one with the highest composite score.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
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

    # Randomly sample 50 indices to label
    num_to_sample = min(50, len(rows))
    indices_to_label = random.sample(range(len(rows)), num_to_sample)
    
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
                    processed_row.append(float(val))
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
    
    print("Optimization Result:")
    print(f"The best working arrangement found is at row index: {best_idx}")
    print("This selection was determined by sampling 50 staff members and identifying")
    print("the one with the highest tenure-based performance score.")
