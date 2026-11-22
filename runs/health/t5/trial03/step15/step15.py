import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that do NOT significantly correlate with poor performance.
    These are the settings that can be left at factory defaults without hurting anything.
    We compare the distribution of input values in the worst 25% of rows
    against the rest. If the distributions are statistically the same,
    the setting is 'safe' to ignore.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Score all rows by ydist (lower is better)
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist and pick the worst 25%
    scored.sort(key=lambda x: x[0], reverse=True)
    n_worst = len(rows) // 4
    worst = [x[1] for x in scored[:n_worst]]
    rest = [x[1] for x in scored[n_worst:]]
    
    # Identify input columns (those not ending in +, -, or !)
    input_indices = [
        i for i, name in enumerate(header) 
        if not (name.endswith('+') or name.endswith('-') or name.endswith('!'))
    ]
    
    # A setting is 'safe' if the distribution in the worst rows is 
    # statistically indistinguishable from the rest.
    safe_settings = []
    for i in input_indices:
        col = tbl.cols[i]
        if isinstance(col, ezr.Num):
            xs = [r[i] for r in worst if r[i] != "?"]
            ys = [r[i] for r in rest if r[i] != "?"]
            if len(xs) > 5 and len(ys) > 5:
                if ezr.same(sorted(xs), sorted(ys)):
                    safe_settings.append(header[i])
        else:
            # For symbolic, check if the distribution of values is similar
            # If the most common value is the same, we consider it 'safe'
            w_counts = {}
            for r in worst: w_counts[r[i]] = w_counts.get(r[i], 0) + 1
            r_counts = {}
            for r in rest: r_counts[r[i]] = r_counts.get(r[i], 0) + 1
            
            w_top = max(w_counts, key=w_counts.get) if w_counts else None
            r_top = max(r_counts, key=r_counts.get) if r_counts else None
            
            if w_top == r_top:
                safe_settings.append(header[i])
                
    return safe_settings

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    safe = blame(header, rows)
    
    print("Analysis: Which settings can be left at factory defaults?")
    if safe:
        print(f"The following settings do not significantly impact performance: {', '.join(safe)}")
        print("You can safely leave these at their default values.")
    else:
        print("All settings appear to have a significant impact on performance.")
