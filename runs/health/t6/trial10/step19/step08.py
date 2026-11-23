import ezr
import step01

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its ydist,
    staying within the provided lever constraints.
    """
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_rows = list(ezr.csv(filename))
    tbl = ezr.Tbl(all_rows)
    
    best_ydist = ezr.ydist(tbl, row)
    best_change = {}

    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        
        candidates = []
        if isinstance(allowed, (tuple, list)) and not isinstance(allowed, str):
            # If it's a range (low, high)
            if len(allowed) == 2 and isinstance(allowed[0], (int, float)):
                low, high = allowed
                # Try 5 steps within the range
                for i in range(5):
                    val = low + (high - low) * (i / 4.0)
                    candidates.append(val)
            else:
                # It's a list of categorical options
                candidates = allowed
        
        for val in candidates:
            if val == row[idx]:
                continue
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
    
    levers = {
        "N_estimators": (50, 200),
        "criterion": ["absolute_error", "poisson", "squared_error"],
        "Min_sample_leaves": (1, 20),
        "Max_depth": (1, 20)
    }
    
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
