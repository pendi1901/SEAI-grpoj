import ezr
import step05

def blame(header, rows):
    """
    Identifies which input settings contribute most to poor performance.
    We compare the distribution of input values in the worst 25% of rows
    against the rest of the data. If the distributions are indistinguishable,
    the setting can be left at default without hurting performance.
    
    The customer asks: "Which settings can I leave at the factory default 
    without hurting anything?"
    This is equivalent to finding the input columns where the distribution 
    of values in the 'worst' rows is NOT significantly different from the 
    distribution in the 'rest' of the rows.
    """
    # Create a table to use ydist for ranking
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Rank rows by ydist (higher ydist = worse performance)
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n_worst = len(rows) // 4
    worst = [x[1] for x in scored[:n_worst]]
    rest = [x[1] for x in scored[n_worst:]]
    
    # For each input column, check if the distribution in 'worst'
    # is significantly different from 'rest'.
    # If they ARE the same, the setting is not a culprit for poor performance.
    safe_settings = []
    for col in tbl.x:
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        # If distributions are the same, this column is safe to leave at default
        if ezr.same(w_vals, r_vals):
            safe_settings.append(col.txt)
            
    return safe_settings

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    results = blame(header, rows)
    
    print("Analysis of settings that can be left at factory defaults:")
    if results:
        print(f"The following settings do not significantly impact performance: {', '.join(results)}")
        print("You can safely leave these at their default values.")
    else:
        print("All settings appear to impact performance; no settings are safe to ignore.")
        
    exit(0)
