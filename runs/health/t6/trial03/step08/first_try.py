import ezr
import step01
import step02
import random

def fix(header, row, levers):
    """
    Find the smallest change to settings that improves the row's ydist
    without violating the constraints defined in 'levers'.
    """
    # Create a table to calculate ydist
    # We use the full data to establish the context for what is "good"
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header_data = data[0]
    rows_data = data[1:]
    tbl = ezr.Tbl(data)

    best_change = {}
    min_dist = ezr.ydist(tbl, row)
    
    # Try changing each lever to a new valid value
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            # Try a few points in the range
            low, high = allowed
            candidates = [low, (low + high) / 2, high]
            candidates = [c for c in candidates if c != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Check if this new configuration is better
            d = ezr.ydist(tbl, new_row)
            if d < min_dist:
                min_dist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on column types
    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }
    
    # Pick a "bad" row (e.g., one with high ydist)
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
