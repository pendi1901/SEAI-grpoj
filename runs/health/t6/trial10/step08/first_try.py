import ezr
import step01
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its ydist,
    staying within the provided lever constraints.
    """
    # Create a dummy table to use ydist and norm functions
    # We need a table with at least some data to define the normalization bounds
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_rows = list(ezr.csv(filename))
    tbl = ezr.Tbl(all_rows)
    
    best_row = list(row)
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}

    # Try changing each lever one by one
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, tuple):  # Numeric (low, high)
            low, high = allowed
            # Try a few points in the range
            for i in range(1, 4):
                val = low + (high - low) * (i / 4)
                candidates.append(val)
        else:  # Symbolic (list of strings)
            candidates = [v for v in allowed if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            new_ydist = ezr.ydist(tbl, new_row)
            
            # We want to minimize ydist (closer to ideal)
            if new_ydist < best_ydist:
                best_ydist = new_ydist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_rows = list(ezr.csv(filename))
    header = all_rows[0]
    rows = all_rows[1:]
    
    # Define levers based on column types
    levers = {
        "N_estimators": (50, 200),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Max_depth": (1, 20)
    }
    
    # Pick a row that is performing poorly (high ydist)
    tbl = ezr.Tbl(all_rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    change = fix(header, bad_row, levers)
    
    print("Optimization recommendation for poor performing setup:")
    if change:
        for col, val in change.items():
            print(f"Change '{col}' to {val}")
    else:
        print("No improvement found within the given constraints.")
