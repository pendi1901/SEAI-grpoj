import ezr
import step01
import step05
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its ydist.
    We search for a change in one lever that minimizes ydist.
    """
    # Load data to build a reference table for ydist calculations
    data = list(ezr.csv("Health-ClosedIssues0000.train.csv"))
    header_data = data[0]
    rows_data = data[1:]
    tbl = ezr.Tbl(data)
    
    best_change = {}
    min_ydist = float('inf')
    
    # Try changing each lever one by one
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low + (high - low) * i / 4 for i in range(5)]
            candidates = [c for c in candidates if abs(c - original_val) > 1e-3]
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            
            # Calculate ydist for the modified row
            # We use the table's column definitions to normalize
            d = ezr.ydist(tbl, new_row)
            
            if d < min_ydist:
                min_ydist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    tbl = ezr.Tbl(data)
    
    # Identify a "bad" row (e.g., one with high ydist)
    scored = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    bad_row = scored[-1]
    
    # Define levers based on input columns (not goals)
    levers = {
        "N_estimators": (10, 200),
        "criterion": ["squared_error", "absolute_error", "friedman_mse", "poisson"],
        "Min_sample_leaves": (1, 20),
        "Min_impurity_decrease": (0, 10),
        "Max_depth": (1, 20)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Analysis:")
    print(f"Bad row identified with ydist: {ezr.ydist(tbl, bad_row):.4f}")
    print("Recommended change to improve performance:")
    for col, val in recommendation.items():
        print(f" - Change '{col}' to {val}")
    
    # Verify improvement
    new_row = list(bad_row)
    for col, val in recommendation.items():
        new_row[header.index(col)] = val
    print(f"New predicted ydist: {ezr.ydist(tbl, new_row):.4f}")
