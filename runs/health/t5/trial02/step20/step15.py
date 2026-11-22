import ezr
import random

def blame(header, rows):
    """
    Identify input columns that have the least impact on performance.
    We compare the distribution of input values in the worst 25% of rows
    against the rest of the data. Columns where the distributions are
    statistically indistinguishable (using the 'same' test) are the
    ones that can be left at factory defaults.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the worst performers
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending (worst first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n_worst = max(1, len(rows) // 4)
    worst = [x[1] for x in scored[:n_worst]]
    rest = [x[1] for x in scored[n_worst:]]
    
    # Identify input columns (skip goals)
    input_cols = [c for c in tbl.x]
    
    safe_cols = []
    for col in input_cols:
        # Extract values for this column from worst and rest
        vals_w = [r[col.at] for r in worst if r[col.at] != "?"]
        vals_r = [r[col.at] for r in rest if r[col.at] != "?"]
        
        # If the distributions are the same, the column doesn't 'blame' the bad performance
        if ezr.same(vals_w, vals_r):
            safe_cols.append(header[col.at])
            
    return safe_cols

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    safe_settings = blame(header, rows)
    
    print("Analysis of settings that can be left at factory defaults:")
    if safe_settings:
        print("The following settings do not significantly impact performance and can be left at defaults:")
        for name in safe_settings:
            print(f"- {name}")
    else:
        print("All settings appear to have a significant impact on performance.")
