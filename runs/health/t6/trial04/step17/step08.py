import ezr
import step01

def fix(header, row, levers):
    """
    Finds the smallest change to a bad row that improves its ydist 
    without increasing the 'N_estimators' (to keep it from getting slower).
    """
    file_path = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(file_path))
    tbl = ezr.Tbl(all_data)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Current N_estimators index is 3
    n_est_idx = 3
    current_n_est = row[n_est_idx]
    
    for name, allowed in levers.items():
        if name not in header:
            continue
        at = header.index(name)
        original_val = row[at]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Generate a few points in the range to test
            candidates = [low + (high - low) * i / 4 for i in range(5)]
            candidates = [c for c in candidates if abs(c - original_val) > 1e-6]
            
        for val in candidates:
            # Constraint: Do not increase N_estimators
            if name == "N_estimators" and val > current_n_est:
                continue
                
            new_row = list(row)
            new_row[at] = val
            
            new_ydist = ezr.ydist(tbl, new_row)
            if new_ydist < best_ydist:
                best_ydist = new_ydist
                best_change = {name: val}
                
    return best_change

if __name__ == "__main__":
    file_path = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(file_path))
    header = all_data[0]
    rows = all_data[1:]
    
    levers = {
        "N_estimators": (50, 200),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Max_depth": (1, 20)
    }
    
    tbl = ezr.Tbl(all_data)
    # Find a bad row (high ydist)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization recommendation for the poor-performing configuration:")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Change '{col}' to {val} to improve performance.")
    else:
        print("No improvement found within constraints.")
