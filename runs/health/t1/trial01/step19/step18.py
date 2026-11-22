import csv

def fix(header, row, levers):
    """
    Finds the single best lever change to improve a 'bad' row.
    A row is better if its goals are closer to their best (min for -, max for +).
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        # Normalize goals: MRE- (min), ACC+ (max), PRED40+ (max)
        # We use a simple heuristic: lower MRE, higher ACC/PRED is better.
        # Since we don't have global bounds, we treat the row's own values 
        # as the baseline for improvement.
        scores = []
        for i in goal_indices:
            val = r[i]
            if header[i].endswith('-'):
                scores.append(-val)
            else:
                scores.append(val)
        return sum(scores) / len(scores)

    best_change = {}
    best_score = -float('inf')

    # Try changing exactly one lever
    for col, allowed in levers.items():
        idx = header.index(col)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, tuple):  # Numeric range (low, high)
            low, high = allowed
            # Test 5 points in the range
            for i in range(5):
                val = low + (high - low) * (i / 4.0)
                if val != original_val:
                    candidates.append(val)
        else:  # Symbolic list
            for val in allowed:
                if val != original_val:
                    candidates.append(val)
        
        for val in candidates:
            new_row = row[:]
            new_row[idx] = val
            score = get_score(new_row)
            if score > best_score:
                best_score = score
                best_change = {col: val}
                
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
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)

        # Define levers
        levers = {
            'N_estimators': (50.0, 200.0),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1.0, 20.0),
            'Min_impurity_decrease': (0.0, 10.0),
            'Max_depth': (1.0, 20.0)
        }

        # Pick a bad row (high MRE-)
        mre_idx = header.index('MRE-')
        bad_row = max(rows, key=lambda r: r[mre_idx])
        
        recommendation = fix(header, bad_row, levers)
        
        print("To improve your setup, we recommend changing only one setting:")
        for col, val in recommendation.items():
            print(f"Update '{col}' to {val}")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
