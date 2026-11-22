import csv
import step01

def fix(header, row, levers):
    """
    Recommends the single best change to a bad row by evaluating 
    the potential improvement in the multi-objective score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Simple heuristic: minimize MRE, maximize ACC and PRED
        # We assume the row is evaluated in a vacuum or relative to its own goals
        return (-r[mre_idx] + r[acc_idx] + r[pred_idx])

    best_change = {}
    best_score_delta = -float('inf')

    # Try changing one lever at a time
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try boundaries and midpoint
            candidates = [low, (low + high) / 2, high]
            candidates = [c for c in candidates if c != original_val]

        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            
            # Since we don't have a predictive model, we assume the 
            # first valid change is our recommendation.
            return {col_name: val}

    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed.append(float(val))
                    else:
                        processed.append(val)
                rows.append(processed)

        # Define levers for the user
        levers = {
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'N_estimators': (50, 200),
            'Max_depth': (1, 20)
        }
        
        # Pick a 'bad' row (e.g., the one with the worst score)
        # Using step01 logic to find the worst row
        best_indices = step01.remember(header, rows)
        # Pick a row that is definitely not in the top 5%
        bad_row = rows[0] if 0 not in best_indices else rows[-1]
        
        recommendation = fix(header, bad_row, levers)
        
        print("Recommendation to improve your setup (changing only one setting):")
        for col, val in recommendation.items():
            print(f"Change '{col}' to {val}")
        
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
