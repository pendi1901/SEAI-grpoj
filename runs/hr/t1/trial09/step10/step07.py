import csv
import random

def choose(header, rows, label):
    """
    Finds the best row by sampling 50 rows, labeling them to get their 
    true goal values, and returning the index of the one with the highest 
    tenure score.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # We can label at most 50 rows.
    # We pick 50 random indices to sample the dataset.
    sample_size = min(50, len(rows))
    indices_to_sample = random.sample(range(len(rows)), sample_size)
    
    best_idx = -1
    best_score = -float('inf')
    
    for idx in indices_to_sample:
        # Get true goal values via label()
        true_goals = label(idx)
        
        # Calculate score: sum of '+' goals minus sum of '-' goals
        current_score = 0
        for i, goal_val in zip(goal_indices, true_goals):
            if header[i].endswith('+'):
                current_score += goal_val
            else:
                current_score -= goal_val
        
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
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    # Define the label function for the harness
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    def label(i):
        return [rows[i][idx] for idx in goal_indices]
    
    # Mask the goal columns
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    best_index = choose(header, rows, label)
    
    print(f"Analysis complete.")
    print(f"The best working arrangement found is at row index: {best_index}")
    print("This row was identified as having the highest tenure-related score among the 50 sampled employees.")
