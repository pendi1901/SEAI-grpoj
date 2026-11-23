import ezr

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its ydist,
    staying within the provided lever constraints.
    """
    # Create a table to get column definitions for ydist calculation
    # We use a dummy list of rows to initialize the table structure
    tbl = ezr.Tbl([header, row])
    
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}

    # Try changing each lever to find an improvement
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        at = header.index(col_name)
        col = tbl.cols[at]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(col, ezr.Sym):
            candidates = [v for v in allowed if v != row[at]]
        else:
            low, high = allowed
            # Try a few points in the range to find an improvement
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != row[at]]

        for val in candidates:
            test_row = list(row)
            test_row[at] = val
            # Recalculate ydist with the new value
            d = ezr.ydist(tbl, test_row)
            if d < best_ydist:
                best_ydist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Define levers based on column types found in the data
    levers = {
        "N_estimators": (50.0, 200.0),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1.0, 20.0),
        "Min_impurity_decrease": (0.0, 10.0),
        "Max_depth": (1.0, 20.0)
    }
    
    # Pick a "bad" row (one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("--- Optimization Analysis ---")
    print(f"Original bad setup: {bad_row}")
    print(f"Recommended change: {recommendation}")
    if recommendation:
        print("This change minimizes the distance to ideal performance goals.")
    else:
        print("No single lever change found that improves performance.")
