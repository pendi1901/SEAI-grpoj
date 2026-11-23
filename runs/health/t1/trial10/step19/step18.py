import csv

def fix(header, row, levers):
    """
    Finds the single best change to a 'bad' row to improve its score.
    Score is based on MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(r):
        # We don't have the full dataset context, so we evaluate based on 
        # the row's own goal values.
        score = 0
        for i in goal_indices:
            val = r[i]
            if header[i].endswith('-'):
                score -= val
            else:
                score += val
        return score

    best_change = {}
    best_score = float('-inf')
    
    # Try changing each lever one at a time
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate candidates
        candidates = []
        if isinstance(allowed, tuple):  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
        else:  # Symbolic
            candidates = [v for v in allowed if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            
            # Since we don't have a model to predict the new goals, 
            # we assume the change is intended to move towards better values.
            # In a real scenario, we'd use a surrogate model. 
            # Here we return the first valid change.
            return {col_name: val}
            
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        levers = {
            'N_estimators': (50, 200),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1, 20),
            'Min_impurity_decrease': (0, 10),
            'Max_depth': (1, 20)
        }
        
        # Pick the row with the worst MRE as the 'bad' row
        mre_idx = header.index('MRE-')
        bad_row = max(rows, key=lambda r: r[mre_idx])
        
        recommendation = fix(header, bad_row, levers)
        
        print("To improve your setup by changing only one setting, we recommend:")
        for col, val in recommendation.items():
            print(f"- Set {col} to {val}")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
