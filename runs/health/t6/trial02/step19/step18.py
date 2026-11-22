import ezr

def fix(header, row, levers):
    """
    Finds the best single-lever change to improve the row's ydist.
    We evaluate potential changes by creating a temporary table context
    to ensure ydist calculations are consistent with the dataset.
    """
    # Create a table to use ydist. We use the header to define columns.
    # Note: The harness expects a valid row, so we use a dummy table
    # to calculate the relative improvement.
    tbl = ezr.Tbl([header])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        at = header.index(col_name)
        
        candidates = []
        if isinstance(allowed, list):
            candidates = [v for v in allowed if v != row[at]]
        elif isinstance(allowed, tuple):
            low, high = allowed
            # Try a few points within the range to find an improvement
            # Using 3 points: low, mid, high
            mid = (low + high) / 2.0
            candidates = [v for v in [low, mid, high] if v != row[at]]
            
        for val in candidates:
            new_row = list(row)
            new_row[at] = val
            
            # Calculate new ydist
            new_ydist = ezr.ydist(tbl, new_row)
            
            if new_ydist < best_ydist:
                best_ydist = new_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Define levers based on the problem description
    levers = {
        "N_estimators": (10.0, 200.0),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1.0, 20.0),
        "Min_impurity_decrease": (0.0, 10.0),
        "Max_depth": (1.0, 20.0)
    }
    
    # Identify a "bad" row (high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Recommendation for bad configuration:")
    if recommendation:
        for col, val in recommendation.items():
            print(f"  Change '{col}' to {val}")
    else:
        print("  No single-lever change found to improve performance.")
