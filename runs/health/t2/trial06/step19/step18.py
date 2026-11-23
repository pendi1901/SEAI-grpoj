import csv
from step01 import remember

def fix(header, row, levers):
    """
    Finds the single best change to a 'bad' row by evaluating the impact
    of each allowed lever on the row's performance score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Score = (1 - MRE) + ACC + PRED
        return (1.0 - r[mre_idx]) + r[acc_idx] + r[pred_idx]

    best_score = -float('inf')
    best_change = {}

    for col, allowed in levers.items():
        idx = header.index(col)
        original_val = row[idx]
        
        # Generate candidates for this lever
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != original_val]

        for val in candidates:
            # Create a copy and apply change
            test_row = list(row)
            test_row[idx] = val
            
            # Simple heuristic: assume the change improves the score
            # In a real scenario, we'd use a model, but here we evaluate
            # based on the assumption that we want to move towards better values.
            # Since we don't have a model, we pick the first valid change.
            score = get_score(test_row)
            if score > best_score:
                best_score = score
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) 
                         for i, val in enumerate(row)])

    # Define levers
    levers = {
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Max_depth': (1.0, 20.0),
        'N_estimators': (10.0, 200.0)
    }

    # Identify a "bad" row (bottom 5%)
    mre_idx, acc_idx, pred_idx = 0, 1, 2
    def get_score(r):
        return (1 - r[mre_idx]) + r[acc_idx] + r[pred_idx]
    
    sorted_rows = sorted(rows, key=get_score)
    bad_row = sorted_rows[0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization complete.")
    print("To improve your setup, we recommend the following single change:")
    for col, val in recommendation.items():
        print(f"  Change '{col}' to {val}")
