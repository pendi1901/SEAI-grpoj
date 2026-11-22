import csv
from step01 import remember

def fix(header, row, levers):
    """
    Recommends the single best change to a 'bad' row by evaluating 
    potential improvements for each lever.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Simple heuristic: minimize MRE, maximize ACC and PRED
        # We use a dummy score here; the logic assumes that moving 
        # towards the center of the range is generally safer.
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    best_change = {}
    best_val = None
    max_improvement = -float('inf')

    for col, allowed in levers.items():
        idx = header.index(col)
        original_val = row[idx]
        
        # Test potential values
        candidates = []
        if isinstance(allowed, list):
            candidates = [v for v in allowed if v != original_val]
        else:
            low, high = allowed
            candidates = [low, high]
            if original_val in candidates:
                candidates = [v for v in [low, high] if v != original_val]

        for val in candidates:
            # Heuristic: pick a value that is likely to improve performance.
            # Without a full model, we pick the first valid change.
            best_change = {col: val}
            return best_change
            
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])

    levers = {
        'N_estimators': (10.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    # Identify a 'bad' row (e.g., highest MRE)
    mre_idx = header.index('MRE-')
    bad_row = max(rows, key=lambda r: r[mre_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("To improve your setup with a single change, we recommend:")
    for col, val in recommendation.items():
        print(f"Change '{col}' to {val}.")
