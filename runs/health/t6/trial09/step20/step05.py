import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of inputs in the worst 10% of rows
    against the rest of the rows.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Score all rows by ydist (lower is better)
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending to get the worst rows
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Define worst 10%
    n_worst = max(1, len(rows) // 10)
    worst_rows = [x[1] for x in scored[:n_worst]]
    other_rows = [x[1] for x in scored[n_worst:]]
    
    # For each input column, check if the distribution in 'worst' is 
    # significantly different from 'others' using ezr.same
    # If they are NOT the same, that column is a candidate for "blame"
    blamed = []
    for col in tbl.x:
        worst_vals = [r[col.at] for r in worst_rows if r[col.at] != "?"]
        other_vals = [r[col.at] for r in other_rows if r[col.at] != "?"]
        
        if not worst_vals or not other_vals:
            continue
            
        # If the distributions are different, this column might be causing the bad performance
        if not ezr.same(worst_vals, other_vals):
            blamed.append(col.txt)
            
    return blamed

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    results = blame(header, rows)
    
    print("Analysis of settings contributing to poor performance:")
    if results:
        print("The following input settings show significantly different distributions")
        print("in the worst-performing setups compared to the rest:")
        for col in results:
            print(f" - {col}")
    else:
        print("No specific input settings were found to be statistically distinct in the worst setups.")
        
    exit(0)
