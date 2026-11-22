import csv
from step02 import guess

def fix(header, row, levers):
    """
    Finds the single best change to a 'bad' row to improve its predicted performance.
    Uses the model from step02 to estimate the impact of changing one lever.
    Optimized to avoid re-reading the file or re-training the model repeatedly.
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    # Load data once
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_f = next(reader)
        for r in reader:
            processed = [float(val) if header_f[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth'] else val for i, val in enumerate(r)]
            rows.append(processed)

    # Pre-calculate baseline score using the model once
    # We use the guess function to predict MRE- for the current row
    # To speed up, we only predict once for the original row
    baseline_mre = guess(header, rows, [row])[0]
    baseline_score = (1.0 - baseline_mre) + row[idx_acc] + row[idx_pred]

    best_change = {}
    best_score = baseline_score

    # Try changing one lever at a time
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, tuple):
            low, high = allowed
            # Use fewer candidates to ensure speed
            candidates = [low, (low + high) / 2, high]
        else:
            candidates = allowed

        for val in candidates:
            if val == original_val:
                continue
            
            new_row = list(row)
            new_row[idx] = val
            
            # Predict MRE- for the new configuration
            # Note: guess() is called on a single row, which is fast
            new_mre = guess(header, rows, [new_row])[0]
            new_score = (1.0 - new_mre) + new_row[idx_acc] + new_row[idx_pred]
            
            if new_score > best_score:
                best_score = new_score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth'] else val for i, val in enumerate(row)]
            rows.append(processed)

    levers = {
        'N_estimators': (10.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    # Fix the last row as a demonstration
    bad_row = rows[-1]
    recommendation = fix(header, bad_row, levers)
    
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Recommended change: Set '{col}' to {val}.")
    else:
        print("No valid improvement found.")
