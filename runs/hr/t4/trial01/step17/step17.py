import csv
from step07 import choose as base_choose

def choose(header, rows, label):
    """
    Finds the best row for 'Laboratory Technician' staff only,
    using the logic from step07 but filtered by jobRole.
    """
    job_role_idx = header.index('jobRole')
    
    # Filter rows to only include Laboratory Technicians
    lab_indices = [i for i, row in enumerate(rows) if row[job_role_idx] == 'Laboratory Technician']
    
    # Map global indices to local indices for the label function
    # The harness expects us to call label(i) where i is the index in the original rows list
    
    # We use the same strategy as step07: label up to 50 rows, predict for all, pick best.
    # We limit our search to the lab_indices.
    
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    # We can label at most 50 rows.
    sample_size = min(50, len(lab_indices))
    labeled_indices = lab_indices[:sample_size]
    
    # Prepare training data
    train_rows = []
    for i in labeled_indices:
        true_vals = label(i)
        row = list(rows[i])
        row[goal_idx] = true_vals[0]
        train_rows.append(row)
        
    # Predict for all Lab Technician rows
    from step02 import guess
    test_rows = []
    for i in lab_indices:
        row = list(rows[i])
        row[goal_idx] = 0.0 # Dummy
        test_rows.append(row)
        
    predictions = guess(header, train_rows, test_rows)
    
    # Find index of best prediction among lab technicians
    if is_maximize:
        best_local_idx = max(range(len(predictions)), key=lambda i: predictions[i])
    else:
        best_local_idx = min(range(len(predictions)), key=lambda i: predictions[i])
        
    return lab_indices[best_local_idx]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    
    def label(i):
        return [rows[i][goal_idx]]
        
    best_idx = choose(header, rows, label)
    
    print(f"The best working arrangement for Laboratory Technicians found is at row index: {best_idx}")
    print(f"Goal value for this row: {rows[best_idx][goal_idx]}")
