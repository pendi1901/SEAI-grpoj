import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the 'worst' rows 
    against the 'best' rows. Columns where the distributions differ 
    significantly are identified as the culprits.
    """
    # Create a table to use ezr's distance and column logic
    tbl = ezr.Tbl([header] + rows)
    
    # Score rows by ydist (lower is better)
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist
    scored.sort(key=lambda x: x[0])
    
    # Define worst 25% and best 25%
    n = len(scored) // 4
    worst = [x[1] for x in scored[-n:]]
    best = [x[1] for x in scored[:n]]
    
    culprits = []
    # Check each input column (x-columns)
    for col in tbl.x:
        at = col.at
        # Extract values for this column
        vals_best = [r[at] for r in best if r[at] != "?"]
        vals_worst = [r[at] for r in worst if r[at] != "?"]
        
        if not vals_best or not vals_worst:
            continue
            
        # If distributions are significantly different, it's a culprit
        # We use ezr.same (cliffs + ks) to check for significant difference
        if not ezr.same(sorted(vals_best), sorted(vals_worst)):
            culprits.append(header[at])
            
    return culprits

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    results = blame(header, rows)
    
    print("Analysis of bad setups:")
    if results:
        print(f"The following settings significantly contribute to poor performance: {', '.join(results)}")
        print("These columns show the largest divergence between the best and worst performing setups.")
    else:
        print("No single setting clearly explains the performance gap.")
