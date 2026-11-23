import ezr
import step01
import step02

def fix(header, row, levers):
    """
    Find the smallest change to settings that improves the row's ydist.
    We iterate through each lever, test possible values, and pick the one
    that minimizes ydist while keeping the change minimal.
    """
    # Create a dummy table to use ydist
    # We need a full dataset to calculate normalized distances correctly
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header_data = next(data_gen)
    all_rows = list(data_gen)
    tbl = ezr.Tbl([header_data] + all_rows)
    
    best_change = {}
    best_ydist = ezr.ydist(tbl, row)
    
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate candidates
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            # Try a few steps between low and high
            low, high = allowed
            for i in range(1, 4):
                val = low + (high - low) * (i / 4)
                candidates.append(val)
        else: # Symbolic (list of strings)
            candidates = [v for v in allowed if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            d = ezr.ydist(tbl, new_row)
            if d < best_ydist:
                best_ydist = d
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Define levers based on column types
    # N_estimators (3), criterion (4), Min_sample_leaves (5), 
    # Min_impurity_decrease (6), Max_depth (7)
    levers = {
        "N_estimators": (50, 200),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Min_impurity_decrease": (0, 10),
        "Max_depth": (1, 20)
    }
    
    # Pick a "bad" row (e.g., one with high ydist)
    tbl = ezr.Tbl([header] + rows)
    bad_row = max(rows, key=lambda r: ezr.ydist(tbl, r))
    
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Analysis:")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve performance, change '{col}' to {val}.")
    else:
        print("No simple change found to improve this configuration.")
    
    exit(0)
