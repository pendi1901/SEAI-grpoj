import csv
from step01 import remember

def fix(header, row, levers):
    """
    Recommends a single change to a 'bad' row to improve its performance.
    It identifies the best-performing rows in the dataset and calculates
    the target values for the allowed levers. It then selects the lever
    that provides the largest shift toward the average of the best rows.
    """
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_file = next(reader)
        for r in reader:
            processed = []
            for i, val in enumerate(r):
                if header_file[i].isupper() or header_file[i] in ['N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed.append(float(val))
                else:
                    processed.append(val)
            rows.append(processed)
            
    best_indices = remember(header_file, rows)
    best_rows = [rows[i] for i in best_indices]
    
    # Calculate target values for levers based on best rows
    targets = {}
    for col in levers:
        idx = header.index(col)
        vals = [r[idx] for r in best_rows]
        if isinstance(vals[0], (int, float)):
            targets[col] = sum(vals) / len(vals)
        else:
            targets[col] = max(set(vals), key=vals.count)
            
    best_change = {}
    max_diff = -1.0
    
    for col, allowed in levers.items():
        idx = header.index(col)
        current_val = row[idx]
        
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], (int, float)): # Symbolic
            if current_val != targets[col] and targets[col] in allowed:
                return {col: targets[col]}
        else: # Numeric (low, high)
            low, high = allowed
            target = max(low, min(high, targets[col]))
            diff = abs(target - current_val)
            if diff > max_diff:
                max_diff = diff
                best_change = {col: target}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i].isupper() or header[i] in ['N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed.append(float(val))
                else:
                    processed.append(val)
            rows.append(processed)
            
    levers = {
        'N_estimators': (10, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }
    
    # Example: Fix the first row
    bad_row = rows[0]
    recommendation = fix(header, bad_row, levers)
    
    print("To improve your setup, we recommend the following single change:")
    for col, val in recommendation.items():
        print(f"Change '{col}' to {val}")
