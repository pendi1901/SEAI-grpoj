import ezr
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its ydist.
    We search for a single lever change that minimizes the ydist.
    """
    # Create a dummy table to use ydist
    # We need a full table to calculate normalization correctly
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header_data = next(data_iter)
    all_rows = list(data_iter)
    tbl = ezr.Tbl([header_data] + all_rows)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    # Try changing each lever
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            # Try a few points in the range
            low, high = allowed
            candidates = [low, (low + high) / 2, high]
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            new_ydist = ezr.ydist(tbl, new_row)
            
            if new_ydist < best_ydist:
                best_ydist = new_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Identify a "bad" row (high ydist)
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    # Define levers based on column types
    levers = {
        "N_estimators": (50, 200),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Min_impurity_decrease": (0, 10),
        "Max_depth": (1, 20)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization recommendation for the worst-performing setup:")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Change '{col}' to {val}.")
    else:
        print("No improvement found within the given lever constraints.")
