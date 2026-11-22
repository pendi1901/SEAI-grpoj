import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, 
    labeling them to find the true goal values, and returning 
    the index of the row with the best performance.
    """
    # Identify goal columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    # We can label at most 50 rows.
    num_to_sample = min(len(rows), 50)
    indices_to_sample = random.sample(range(len(rows)), num_to_sample)
    
    best_idx = -1
    best_score = None
    
    for idx in indices_to_sample:
        # Get true goal values
        goals = label(idx)
        
        # Calculate a normalized score for this row
        # Since we want to maximize '+' and minimize '-', we normalize
        # For simplicity, we use the first goal column provided
        g_idx = goal_indices[0]
        val = goals[0]
        
        # If goal ends in +, higher is better. If -, lower is better.
        # We treat the value as the score.
        if header[g_idx].endswith('-'):
            score = -val
        else:
            score = val
            
        if best_score is None or score > best_score:
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

    # Store original goal values to simulate the label function
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    true_goals = [[row[i] for i in goal_indices] for row in rows]
    
    # Mask goals
    for row in rows:
        for i in goal_indices:
            row[i] = "?"

    labeled_count = 0
    def label(i):
        global labeled_count
        labeled_count += 1
        if labeled_count > 50:
            raise Exception("Limit exceeded")
        return true_goals[i]

    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete.")
    print(f"Best row index found: {best_idx}")
    print(f"Goal values for best row: {true_goals[best_idx]}")
    print("Strategy: Randomly sampled 50 rows to identify the best performing arrangement.")
