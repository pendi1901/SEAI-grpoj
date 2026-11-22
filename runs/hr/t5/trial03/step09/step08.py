import ezr
import random

def fix(header, row, levers):
    """
    Given a 'bad' row, suggest changes to levers to improve its ydist.
    We evaluate potential changes by simulating the impact on the row's 
    predicted ydist using the library's distance metrics.
    """
    # We need a table to access column definitions for normalization
    # We use a minimal table structure to ensure we can calculate ydist
    # The library's ydist relies on the table's y-columns and normalization
    # We build a table from the full dataset to ensure correct normalization
    # (The harness provides the header and row, but we need the context of the data)
    # Since we cannot access the full dataset inside the function, we rely on 
    # the row's own context or assume the library's norm function works on the row.
    
    # Create a dummy table to use the library's distance functions
    # We use a single row table; note that normalization might be limited
    # but it's the only way to use the provided library functions.
    tbl = ezr.Tbl([header, row])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        
        at = header.index(col_name)
        original_val = row[at]
        
        # Generate candidates based on lever type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        elif isinstance(allowed, tuple):  # Numeric (low, high)
            low, high = allowed
            # Try discrete steps in the range
            step = (high - low) / 4
            candidates = [low + i * step for i in range(5)]
            candidates = [c for c in candidates if c != original_val]
            
        for val in candidates:
            # Create a test row with the change
            test_row = list(row)
            test_row[at] = val
            
            # Calculate new ydist
            current_ydist = ezr.ydist(tbl, test_row)
            
            # If this change improves the ydist, keep it
            if current_ydist < best_ydist:
                best_ydist = current_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Define levers based on customer request
    levers = {
        "businessTravel": ["Non-Travel", "Travel_Frequently", "Travel_Rarely"],
        "overTime": ["No", "Yes"],
        "TrainingTimesLastYear": (0.0, 6.0),
        "PercentSalaryHike": (11.0, 25.0),
        "StockOptionLevel": (0.0, 3.0)
    }
    
    # Pick a "bad" row (high ydist) to demonstrate
    tbl = ezr.Tbl(data)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("--- Recommendation for Employee Improvement ---")
    print(f"Original YDist: {ezr.ydist(tbl, bad_row):.2f}")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Recommended change: Set {col} to {val}")
        
        # Verify improvement
        new_row = list(bad_row)
        new_row[header.index(col)] = val
        print(f"New predicted YDist: {ezr.ydist(tbl, new_row):.2f}")
    else:
        print("No beneficial changes found within the provided levers.")
    
    exit(0)
