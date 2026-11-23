import ezr
import random

def fix(header, row, levers):
    """
    Find the smallest change to a 'bad' row that improves its ydist.
    'Smallest change' is defined as the single lever change that results 
    in the lowest ydist.
    """
    # Create a dummy table to use ydist
    # We need a table with at least some data to calculate norms
    # We'll use the row itself as the reference for normalization
    tbl = ezr.Tbl([header, row])
    
    best_row = list(row)
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}
    
    # Try changing each lever one by one
    for col_name, allowed in levers.items():
        at = header.index(col_name)
        original_val = row[at]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(allowed, list): # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else: # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[at] = val
            
            # Evaluate
            current_ydist = ezr.ydist(tbl, new_row)
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Define levers based on column types
    levers = {
        'N_estimators': (10, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }
    
    # Pick a "bad" row (e.g., one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    indexed = sorted([(r, ezr.ydist(tbl, r)) for r in rows], key=lambda x: x[1], reverse=True)
    bad_row = indexed[0][0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis complete.")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve performance, change '{col}' to {val}.")
    else:
        print("No single lever change found that improves performance.")
        
    exit(0)
