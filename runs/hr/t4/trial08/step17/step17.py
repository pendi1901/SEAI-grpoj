import csv
import random
from step02 import guess

def choose(header, rows, label):
    """
    Finds the best working arrangement for 'Laboratory Technician' staff 
    by sampling 50 rows, labeling them, and predicting the best row 
    using a Random Forest model.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    job_role_idx = header.index('jobRole')
    
    # Filter indices for Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[job_role_idx] == 'Laboratory Technician']
    
    # If fewer than 50 lab techs, sample all of them; otherwise sample 50
    sample_size = min(50, len(lab_indices))
    sample_indices = random.sample(lab_indices, sample_size)
    
    # Label the sampled rows
    labeled_data = []
    for idx in sample_indices:
        true_goals = label(idx)
        row_copy = list(rows[idx])
        for i, g_idx in enumerate(goal_indices):
            row_copy[g_idx] = true_goals[i]
        labeled_data.append(row_copy)
    
    # Prepare all rows for prediction. 
    # Note: step02.py's guess() function expects the test rows to have the same 
    # structure as the training data. We must keep the goal columns as '?' 
    # so that step02's transform_row logic correctly skips them.
    test_rows = [list(row) for row in rows]
    
    # Predict goals for all rows
    predictions = guess(header, labeled_data, test_rows)
    
    # Find the best row among Laboratory Technicians
    # We use the first goal column as the primary metric
    target_goal_idx = goal_indices[0]
    is_maximize = header[target_goal_idx].endswith('+')
    
    best_idx = -1
    best_val = -float('inf') if is_maximize else float('inf')
    
    for i in lab_indices:
        val = predictions[i]
        if is_maximize:
            if val > best_val:
                best_val = val
                best_idx = i
        else:
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

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Mask goals for the choose function
    for row in rows:
        for g in goal_indices:
            row[g] = "?"

    def label(i):
        # This is a helper for the harness to retrieve true values
        # In the real scenario, the harness provides the label function
        return [rows[i][g] for g in goal_indices]

    best_index = choose(header, rows, label)
    print(f"The best working arrangement for Laboratory Technicians is found at row index: {best_index}")
    exit(0)
