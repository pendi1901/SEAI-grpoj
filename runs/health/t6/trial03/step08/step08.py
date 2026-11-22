import ezr
import step01

def fix(header, row, levers):
    """
    Find the smallest change to settings that improves the row's ydist
    without violating the constraints defined in 'levers'.
    """
    # Load data to build a model of the objective space
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    # We need a baseline ydist for the current row.
    # Since the row might have '?' in goals, we use the tree-based ranker
    # from step02 to estimate the current performance.
    ranker = ezr.ranker(tbl)
    current_score = ranker(row)
    
    best_change = {}
    best_score = current_score
    
    # Try changing each lever to a new valid value
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Sample points in the range to find an improvement
            candidates = [low, (low + high) / 2, high]
            candidates = [c for c in candidates if c != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Check if this new configuration is better
            new_score = ranker(new_row)
            if new_score < best_score:
                best_score = new_score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on the problem description
    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }
    
    # Pick a "bad" row (high ydist)
    tbl = ezr.Tbl(data)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization recommendation for the current setup:")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Change '{col}' to {val} to improve performance.")
    else:
        print("No single-lever change found to improve performance.")
        
    exit(0)
