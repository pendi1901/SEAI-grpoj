import csv
import random

def choose(header, rows, label):
    """
    Find the best working arrangement by sampling 50 rows, 
    labeling them, and picking the one with the highest aggregate goal score.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Randomly sample 50 indices
    indices = list(range(len(rows)))
    sample_size = min(50, len(rows))
    sampled_indices = random.sample(indices, sample_size)
    
    best_idx = -1
    best_score = -float('inf')
    
    for i in sampled_indices:
        # Get true values for this row
        goals = label(i)
        
        # Calculate a normalized score for the row
        # For '+', we want high values. For '-', we want low values.
        # Since we don't have global min/max easily, we use the raw values 
        # relative to the goal direction.
        current_score = 0
        for j, g_idx in enumerate(goal_indices):
            val = goals[j]
            if header[g_idx].endswith('+'):
                current_score += val
            else:
                current_score -= val
        
        if current_score > best_score:
            best_score = current_score
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    full_data = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            full_data.append(processed)
            
            # Mask goals for the 'rows' passed to choose
            masked = list(processed)
            for i, name in enumerate(header):
                if name.endswith('+') or name.endswith('-'):
                    masked[i] = "?"
            rows.append(masked)
            
    def label(i):
        goal_indices = [idx for idx, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
        return [full_data[i][idx] for idx in goal_indices]
    
    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete. The best working arrangement found is at row index {best_idx}.")
    print("This row was identified as having the highest retention-related metrics among the 50 sampled staff members.")
