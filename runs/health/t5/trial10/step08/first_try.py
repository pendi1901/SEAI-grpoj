import ezr
import random

def fix(header, row, levers):
    """
    Find the smallest change to a bad row that improves its ydist.
    'Smallest' is defined as the minimum xdist from the original row.
    """
    # Create a table to handle normalization and distance calculations
    # We need a context of rows to normalize properly
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    tbl = ezr.Tbl(data)
    
    best_change = {}
    min_xdist = 1e30
    
    # Try changing one lever at a time
    for col_name, allowed in levers.items():
        at = header.index(col_name)
        col = tbl.cols[at]
        original_val = row[at]
        
        # Generate candidates based on type
        candidates = []
        if isinstance(col, ezr.Sym):
            candidates = [v for v in allowed if v != original_val]
        else:
            low, high = allowed
            # Try a few points in the range
            candidates = [low, (low + high) / 2, high]
            candidates = [v for v in candidates if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[at] = val
            
            # Calculate distance from original (cost of change)
            d = ezr.xdist(tbl, row, new_row)
            
            # Check if this change improves the row
            # We use the current row's ydist as a baseline
            if ezr.ydist(tbl, new_row) < ezr.ydist(tbl, row):
                if d < min_xdist:
                    min_xdist = d
                    best_change = {col_name: val}
                    
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a "bad" row (high ydist)
    tbl = ezr.Tbl(data)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    # Define levers based on column types
    levers = {
        'N_estimators': (50, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Recommended change for the bad setup:")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Change '{col}' to {val}")
    else:
        print("No simple improvement found.")
    
    exit(0)
