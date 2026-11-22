import ezr
import step01
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a bad row's settings that improves its ydist.
    We perform a local search by perturbing one lever at a time and checking
    if the resulting ydist improves.
    """
    # Create a dummy table to use ydist
    # We need a table to calculate ydist, so we use the header
    # and a single row to define the column roles.
    tbl = ezr.Tbl([header, row])
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try changing each lever
    for col_name, allowed in levers.items():
        at = header.index(col_name)
        original_val = row[at]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[at] = val
            
            # Calculate new ydist
            # We use the same tbl structure to evaluate the new row
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
    
    # Define levers based on the dataset
    levers = {
        "N_estimators": (10, 200),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Min_impurity_decrease": (0, 10),
        "Max_depth": (1, 20)
    }
    
    # Pick a "bad" row (one with high ydist)
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
