import csv
import random

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, 
    labeling them to get their true goal values, and picking the best one.
    
    Goal columns end in '+' (maximize) or '-' (minimize).
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    
    # Randomly sample 50 indices to label
    indices_to_sample = random.sample(range(len(rows)), min(50, len(rows)))
    
    best_idx = -1
    best_score = float('-inf')
    
    for idx in indices_to_sample:
        # Get true values for this row
        true_goals = label(idx)
        
        # Calculate a normalized score for this row
        # Since we don't have the full distribution, we use the values directly
        # A row is better if '+' goals are high and '-' goals are low.
        # We'll use a simple weighted sum approach.
        current_score = 0
        for i, goal_idx in enumerate(goal_indices):
            val = true_goals[i]
            if header[goal_idx].endswith('+'):
                current_score += val
            else:
                current_score -= val
        
        if current_score > best_score:
            best_score = current_score
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

    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
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
            processed = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed.append(float(val))
                else:
                    processed.append(val)
            original_data.append(processed)

    labeled_count = 0
    def label(i):
        global labeled_count
        labeled_count += 1
        if labeled_count > 50:
            raise ValueError("Limit of 50 labels exceeded.")
        return [original_data[i][idx] for idx in goal_indices]

    best_idx = choose(header, rows, label)
    
    print(f"Analysis complete. Best row index found: {best_idx}")
    print("This row represents the working arrangement that maximizes the goal metrics.")
