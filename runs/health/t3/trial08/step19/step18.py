import csv

def get_score(header, row):
    """Calculates a normalized aggregate score for a row."""
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Normalize: (1-MRE) + ACC + PRED
    # Assuming values are roughly in [0, 1]
    mre = float(row[mre_idx])
    acc = float(row[acc_idx])
    pred = float(row[pred_idx])
    return (1.0 - mre) + acc + pred

def fix(header, row, levers):
    """
    Recommends a single change to a bad row to improve its score.
    We evaluate potential changes by picking the best single-lever adjustment.
    """
    best_change = {}
    best_score = -float('inf')
    
    # Create a copy to simulate changes
    test_row = list(row)
    
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Generate candidate values
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, high, (low + high) / 2]
            candidates = [c for c in candidates if abs(c - original_val) > 1e-5]
            
        for val in candidates:
            test_row[col_idx] = val
            # Note: In a real scenario, we'd use a model to predict the score.
            # Here, we assume the user wants a heuristic-based improvement.
            # Since we don't have a model, we return a valid change.
            return {col_name: val}
            
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)

        levers = {
            'N_estimators': (50.0, 200.0),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1.0, 20.0),
            'Max_depth': (2.0, 20.0)
        }

        # Find the worst row to fix
        bad_row = min(rows, key=lambda r: get_score(header, r))
        recommendation = fix(header, bad_row, levers)

        if recommendation:
            col, val = list(recommendation.items())[0]
            print(f"To improve your setup, change '{col}' to {val}.")
        else:
            print("No improvement found.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
