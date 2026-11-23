import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, labeling them,
    and identifying the one with the highest tenure-based score.
    """
    goal_indices = [i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-')]
    
    # We have 800 rows. We can label 50.
    # We will sample 50 indices to evaluate.
    indices_to_label = random.sample(range(len(rows)), 50)
    
    best_idx = -1
    best_score = -float('inf')
    
    for i in indices_to_label:
        # Get true values for the goals
        true_goals = label(i)
        
        # Calculate score: maximize '+' goals, minimize '-' goals
        score = 0
        for j, goal_idx in enumerate(goal_indices):
            val = true_goals[j]
            col_name = header[goal_idx]
            if col_name.endswith('+'):
                score += val
            elif col_name.endswith('-'):
                score -= val
        
        if score > best_score:
            best_score = score
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Mask goals
    goal_indices = [i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-')]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    # Define label function for the harness
    # We need to keep a copy of original data to provide labels
    original_data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            original_data.append([float(row[i]) if header[i][0].isupper() else row[i] for i in range(len(row))])

    labeled_count = 0
    def label(i):
        global labeled_count
        labeled_count += 1
        if labeled_count > 50:
            raise Exception("Limit exceeded")
        return [original_data[i][idx] for idx in goal_indices]

    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete.")
    print(f"Best row found at index: {best_idx}")
    print(f"This row represents the working arrangement that keeps people longest based on the 50 sampled interviews.")
