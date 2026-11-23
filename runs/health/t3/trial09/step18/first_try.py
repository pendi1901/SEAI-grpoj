import csv

def fix(header, row, levers):
    """
    Recommends a single change to a 'bad' row to improve its performance.
    Evaluates potential changes by calculating the improvement in the 
    multi-objective goal score.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        score = 0
        for i in goal_indices:
            val = r[i]
            if header[i].endswith('-'):
                score -= val
            else:
                score += val
        return score

    best_change = {}
    best_score = get_score(row)
    
    # Try changing one lever at a time
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, list):
            # Symbolic: try all allowed values
            for val in allowed:
                if val != original_val:
                    candidates.append(val)
        else:
            # Numeric: try boundaries and midpoint
            low, high = allowed
            for val in [low, high, (low + high) / 2]:
                if val != original_val:
                    candidates.append(val)
        
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            
            # If the new configuration score is better, track it
            current_score = get_score(new_row)
            if current_score > best_score:
                best_score = current_score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for val in row:
                try:
                    processed.append(float(val))
                except ValueError:
                    processed.append(val)
            rows.append(processed)

    # Define the levers available for change
    levers = {
        'N_estimators': (10.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    def get_score(r):
        s = 0
        for i, name in enumerate(header):
            if name.endswith('-'): s -= r[i]
            elif name.endswith('+'): s += r[i]
        return s

    # Pick a 'bad' row (bottom 10% performance)
    scores = [(get_score(r), i) for i, r in enumerate(rows)]
    scores.sort()
    bad_row_idx = scores[0][1]
    bad_row = rows[bad_row_idx]
    
    recommendation = fix(header, bad_row, levers)
    
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve your setup, we recommend changing '{col}' to {val}.")
    else:
        print("No single-lever change was found to improve the current configuration.")
