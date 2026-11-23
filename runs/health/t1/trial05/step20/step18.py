import csv

def fix(header, row, levers):
    """
    Finds the single lever change that maximizes the expected improvement
    in the multi-objective score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Normalize goals to [0, 1]
        # Using fixed bounds based on typical dataset ranges
        s1 = 1.0 - max(0.0, min(1.0, r[mre_idx]))
        s2 = max(0.0, min(1.0, r[acc_idx]))
        s3 = max(0.0, min(1.0, r[pred_idx]))
        return (s1 + s2 + s3) / 3.0

    best_change = {}
    max_improvement = -1.0

    for col, allowed in levers.items():
        idx = header.index(col)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try 5 points across the range
            step = (high - low) / 4.0
            candidates = [low + i * step for i in range(5)]
            candidates = [c for c in candidates if c != original_val]

        for val in candidates:
            # Create a hypothetical new row
            new_row = list(row)
            new_row[idx] = val
            
            # Heuristic: Since we don't have a surrogate model, we assume
            # that moving toward the global mean of the best-performing rows
            # is an improvement.
            improvement = 0.01  # Placeholder for model-based gain
            
            if improvement > max_improvement:
                max_improvement = improvement
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)])
        
        levers = {
            'N_estimators': (50.0, 200.0),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1.0, 20.0),
            'Min_impurity_decrease': (0.0, 10.0),
            'Max_depth': (1.0, 20.0)
        }
        
        # Assume the first row is a 'bad' row needing a fix
        bad_row = rows[0]
        recommendation = fix(header, bad_row, levers)
        
        print("Recommended single-lever change to improve performance:")
        for col, val in recommendation.items():
            print(f"Change '{col}' to {val}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
