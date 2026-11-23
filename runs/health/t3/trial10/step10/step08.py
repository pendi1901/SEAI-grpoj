import csv
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a bad row's settings to improve performance
    without increasing complexity (assuming N_estimators is a proxy for speed).
    """
    # Identify indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    n_est_idx = header.index('N_estimators')
    
    # Helper to evaluate if a row is "better"
    def get_score(r):
        # Simple heuristic: minimize MRE, maximize ACC and PRED
        # We use placeholders for unknown goals if necessary, but here we assume
        # we are comparing against the provided row's current state.
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    best_change = {}
    
    # Try changing one lever at a time
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        current_val = row[col_idx]
        
        # For numeric, try a small step within range
        if isinstance(allowed, tuple):
            low, high = allowed
            # Try moving towards the middle or a random valid point
            # Here we try a small perturbation
            step = (high - low) * 0.1
            for direction in [-1, 1]:
                new_val = max(low, min(high, current_val + (direction * step)))
                if new_val != current_val:
                    best_change[col_name] = new_val
        
        # For symbolic, try a different value
        elif isinstance(allowed, list):
            for val in allowed:
                if val != current_val:
                    best_change[col_name] = val
                    break
                    
    # Constraint: Do not increase N_estimators (speed proxy)
    if 'N_estimators' in best_change:
        if best_change['N_estimators'] > row[n_est_idx]:
            del best_change['N_estimators']
            
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define levers based on column types
    levers = {
        'N_estimators': (50.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    # Pick a "bad" row (e.g., the one with the worst MRE)
    mre_idx = header.index('MRE-')
    bad_row = max(rows, key=lambda r: r[mre_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Recommendation for improving the setup:")
    for col, val in recommendation.items():
        print(f"- Change {col} to {val}")
    
    exit(0)
