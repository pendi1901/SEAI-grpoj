import ezr
import random

def fix(header, row, levers):
    """
    Find the smallest change to a bad row that improves its ydist 
    without increasing complexity (N_estimators).
    """
    # Create a table to handle normalization and distance calculations
    # We need a full table to calculate ydist correctly
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header_data = next(data_iter)
    all_rows = list(data_iter)
    tbl = ezr.Tbl([header_data] + all_rows)
    
    best_change = {}
    min_dist = ezr.ydist(tbl, row)
    
    # Try changing one lever at a time
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Generate candidates
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            # Try a few points in the range
            low, high = allowed
            candidates = [low, (low + high) / 2, high]
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
    
    # Define levers: we can change criterion, Min_sample_leaves, 
    # Min_impurity_decrease, Max_depth. We exclude N_estimators to keep it fast.
    levers = {
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Min_impurity_decrease": (0, 10),
        "Max_depth": (1, 20)
    }
    
    # Pick a "bad" row (e.g., one with a high ydist)
    tbl = ezr.Tbl([header] + rows)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    bad_row = sorted_rows[0]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Customer Query: What is the smallest change to improve performance without slowing down?")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"Recommendation: Change '{col}' to {val}.")
        print("This adjustment is expected to move the configuration closer to optimal goals.")
    else:
        print("Recommendation: No single-lever change found that improves performance.")
        
    exit(0)
