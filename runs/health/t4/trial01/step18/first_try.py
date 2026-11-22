import csv
from step02 import guess

def fix(header, row, levers):
    """
    Finds the single best change to a 'bad' row to improve its predicted performance.
    Uses the model from step02 to estimate the impact of changing one lever.
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    # We need a reference dataset to train the model for predictions.
    # Since we don't have the full dataset passed in, we load it from the file.
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_f = next(reader)
        for r in reader:
            processed = [float(val) if header_f[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth'] else val for i, val in enumerate(r)]
            rows.append(processed)

    def get_score(r):
        # MRE- is minimized, ACC+ and PRED40+ are maximized
        # We use the model to predict MRE- and use row values for others as a proxy
        # for the impact of the change.
        mre = guess(header, rows, [r])[0]
        acc = r[idx_acc]
        pred = r[idx_pred]
        return (1.0 - mre) + acc + pred

    best_change = {}
    best_score = -float('inf')

    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, tuple):
            low, high = allowed
            # Try a few points in the range
            step = (high - low) / 5
            candidates = [low + i * step for i in range(6)]
        else:
            candidates = allowed

        for val in candidates:
            if val == original_val:
                continue
            new_row = list(row)
            new_row[idx] = val
            
            score = get_score(new_row)
            if score > best_score:
                best_score = score
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

    # Example: Fix the last row
    bad_row = rows[-1]
    recommendation = fix(header, bad_row, levers)
    
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Recommended change: Set '{col}' to {val}.")
    else:
        print("No valid improvement found.")
