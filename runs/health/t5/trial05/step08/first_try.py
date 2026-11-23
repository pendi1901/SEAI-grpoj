import ezr
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its ydist
    without violating the constraints defined in 'levers'.
    """
    # Create a table to use ydist for evaluation
    # We need the full dataset to understand the global context of 'good'
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header_data = next(data_iter)
    all_rows = list(data_iter)
    tbl = ezr.Tbl([header_data] + all_rows)

    best_change = {}
    min_ydist = ezr.ydist(tbl, row)
    
    # Try changing each lever one by one
    for col_name, allowed in levers.items():
        at = header.index(col_name)
        original_val = row[at]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            # Try a few steps within the range
            low, high = allowed
            step = (high - low) / 5
            candidates = [low + i * step for i in range(6)]
            candidates = [c for c in candidates if abs(c - original_val) > 1e-3]
            
        for val in candidates:
            new_row = row[:]
            new_row[at] = val
            new_ydist = ezr.ydist(tbl, new_row)
            
            if new_ydist < min_ydist:
                min_ydist = new_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Define levers based on column types
    levers = {
        "N_estimators": (50, 200),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Min_impurity_decrease": (0, 10),
        "Max_depth": (1, 20)
    }
    
    # Pick a "bad" row (e.g., one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    ranked = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    bad_row = ranked[-1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("--- Optimization Recommendation ---")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve performance, change '{col}' to {ezr.say(val)}.")
    else:
        print("No simple single-lever change found to improve performance.")
