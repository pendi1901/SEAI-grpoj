import ezr
import random

def fix(header, row, levers):
    """
    Find the smallest change to a bad row's settings that improves its ydist.
    We iterate through each lever, try all possible values, and pick the one
    that results in the best ydist improvement.
    """
    # Create a dummy table to use ydist
    # We need a table to calculate ydist, but we don't have the full dataset here.
    # We can use the row itself to initialize a minimal table.
    tbl = ezr.Tbl([header, row])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Determine candidates based on type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Calculate new ydist
            # Since we don't have the full dataset, we assume the model 
            # is static or we are optimizing locally.
            new_ydist = ezr.ydist(tbl, new_row)
            
            if new_ydist < best_ydist:
                best_ydist = new_ydist
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
    
    print("Analysis complete.")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve performance, change '{col}' to {val}.")
    else:
        print("No single-lever change found to improve performance.")
    
    exit(0)
