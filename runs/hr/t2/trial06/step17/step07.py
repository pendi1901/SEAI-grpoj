import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, 
    labeling them to find their true goal values, and returning 
    the index of the row with the highest aggregate score.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # We can label at most 50 rows.
    num_to_sample = min(len(rows), 50)
    indices = random.sample(range(len(rows)), num_to_sample)
    
    best_idx = -1
    best_score = float('-inf')
    
    for idx in indices:
        # Get true values for the goals
        true_goals = label(idx)
        
        # Calculate score: maximize '+' goals, minimize '-' goals
        score = 0
        for i, goal_idx in enumerate(goal_indices):
            val = true_goals[i]
            name = header[goal_idx]
            if name.endswith('+'):
                score += val
            else:
                score -= val
        
        if score > best_score:
            best_score = score
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Define the label function for the harness
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    # Mask the rows
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    best_row_idx = choose(header, rows, label)
    
    print(f"The best working arrangement found is at row index: {best_row_idx}")
    print("This selection was based on an in-depth analysis of 50 sampled employee records.")
