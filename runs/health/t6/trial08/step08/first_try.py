import ezr
import step01
import step05

def fix(header, row, levers):
    """
    Find the smallest change to a bad row that improves its ydist 
    without increasing the setup size (N_estimators).
    """
    tbl = ezr.Tbl([header] + [row])
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # We want to improve ydist (lower is better)
    # We must not increase N_estimators (index 3)
    n_est_idx = header.index('N_estimators')
    current_n_est = row[n_est_idx]

    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try all allowed values
        for val in allowed:
            if val == original_val:
                continue
            
            # Constraint: Do not increase N_estimators
            if idx == n_est_idx and val > current_n_est:
                continue
                
            # Create a candidate row
            candidate = list(row)
            candidate[idx] = val
            
            # Evaluate
            cand_ydist = ezr.ydist(tbl, candidate)
            if cand_ydist < best_ydist:
                best_ydist = cand_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Identify a "bad" row (e.g., one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    bad_row = scored[-1][1]
    
    # Define levers based on column types
    levers = {
        'N_estimators': (10, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }
    
    # Prepare allowed values for the function
    allowed_levers = {}
    for name, val in levers.items():
        if isinstance(val, tuple):
            # Generate a few steps for numeric ranges
            low, high = val
            allowed_levers[name] = [low + (high - low) * i / 4 for i in range(5)]
        else:
            allowed_levers[name] = val
            
    recommendation = fix(header, bad_row, allowed_levers)
    
    print("Analysis complete.")
    if recommendation:
        print(f"To improve performance, change: {recommendation}")
    else:
        print("No simple change found to improve performance within constraints.")
    
    exit(0)
