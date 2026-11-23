import ezr

def fix(header, row, levers):
    """
    Find the single best change to a bad row that improves its ydist.
    """
    # Load data to build a model for ydist calculation
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header_data = next(data_iter)
    all_rows = list(data_iter)
    tbl = ezr.Tbl([header_data] + all_rows)
    
    best_change = {}
    # Current distance of the bad row
    min_dist = ezr.ydist(tbl, row)
    
    # Try changing one lever at a time
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
            # Try a few points in the range to find an improvement
            # Ensure we stay within the provided bounds
            candidates = [low, (low + high) / 2.0, high]
            candidates = [v for v in candidates if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            
            # Check if this change improves the row
            new_dist = ezr.ydist(tbl, new_row)
            if new_dist < min_dist:
                min_dist = new_dist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Define levers based on the dataset structure
    # Ensure these match the column names in the CSV exactly
    levers = {
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Min_impurity_decrease": (0, 10),
        "Max_depth": (1, 20),
        "N_estimators": (10, 200)
    }
    
    # Pick a "bad" row (one with a high ydist)
    tbl = ezr.Tbl([header] + rows)
    # Sort by ydist descending to find the worst rows
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = sorted_rows[0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Query: Fix my setup, but I am only allowed to change one setting.")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Recommendation: Change '{col}' to {val}.")
        print("This single adjustment is expected to improve your configuration's performance.")
    else:
        print("Recommendation: No single-lever change found that improves performance.")
        
    exit(0)
