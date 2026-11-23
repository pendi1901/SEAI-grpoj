import csv
import random
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best working arrangement by sampling 50 rows, 
    labeling them to get true goal values, and predicting 
    the best row based on a Random Forest model.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Randomly sample 50 indices to label
    sample_indices = random.sample(range(len(rows)), min(50, len(rows)))
    
    # Label the sampled rows
    labeled_data = []
    for idx in sample_indices:
        true_goals = label(idx)
        # Create a copy of the row with true goals filled in
        row_copy = list(rows[idx])
        for i, g_idx in enumerate(goal_indices):
            row_copy[g_idx] = true_goals[i]
        labeled_data.append(row_copy)
    
    # Train a model on the 50 labeled rows to predict goals for all rows
    # We use the guess logic from step02 but adapted for multiple goals
    # For simplicity, we predict the first goal column as the primary metric
    target_goal_idx = goal_indices[0]
    
    # Prepare training data for the model
    # We use the 50 labeled rows as training set
    predictions = guess(header, labeled_data, rows)
    
    # Find the row with the best predicted goal value
    # If goal ends in '+', we want max; if '-', we want min
    is_maximize = header[target_goal_idx].endswith('+')
    
    best_idx = 0
    if is_maximize:
        best_val = -float('inf')
        for i, val in enumerate(predictions):
            if val > best_val:
                best_val = val
                best_idx = i
    else:
        best_val = float('inf')
        for i, val in enumerate(predictions):
            if val < best_val:
                best_val = val
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

    # Define the label function for the harness
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    def label(i):
        return [rows[i][g] for g in goal_indices]

    # Mask goals for the choose function
    for row in rows:
        for g in goal_indices:
            row[g] = "?"

    best_index = choose(header, rows, label)
    print(f"The best working arrangement is found at row index: {best_index}")
