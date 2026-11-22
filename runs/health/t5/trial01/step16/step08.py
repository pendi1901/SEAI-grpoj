import ezr
import random

def fix(header, row, levers):
    """
    Find the smallest change to a 'bad' row that improves its ydist 
    without violating the constraints defined in 'levers'.
    """
    # Build a table to calculate ydist
    # We need the full dataset to establish the context for ydist normalization
    # Since we don't have the full dataset passed in, we assume the caller
    # expects us to use the global context or a minimal table.
    # To ensure ydist works, we need the column definitions.
    tbl = ezr.Tbl([header])
    
    # Re-populate the table with the row to ensure column stats are initialized
    # (Though for a single row, ydist will be relative to the column's own stats)
    ezr.addRow(tbl, row)
    
    current_ydist = ezr.ydist(tbl, row)
    best_change = {}
    min_dist = float('inf')
    
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
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            candidates = [c for c in candidates if c != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Check if this change improves ydist
            new_ydist = ezr.ydist(tbl, new_row)
            
            if new_ydist < current_ydist:
                # We want the smallest change. 
                # For numeric, distance is abs(new-old). For symbolic, 1.
                dist = abs(val - original_val) if isinstance(val, (int, float)) else 1
                if dist < min_dist:
                    min_dist = dist
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
        
    # Define levers based on the dataset structure
    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Max_depth': (1, 20)
    }
    
    # Find a 'bad' row (e.g., one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Analysis:")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve performance, change '{col}' to {val}.")
    else:
        print("No simple single-lever change found to improve performance.")
        
    exit(0)
