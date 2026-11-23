import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the bottom 25% of rows based on ydist.
    We then compare the distribution of input values in the worst rows 
    against the rest of the data.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist (higher is worse)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    split_idx = len(scored) // 4
    worst = [x[1] for x in scored[:split_idx]]
    rest = [x[1] for x in scored[split_idx:]]
    
    # For each input column, check if the distribution of values in 'worst'
    # is significantly different from 'rest'.
    # We use the same logic as step03 (certify) to find columns that matter.
    important_cols = []
    for col in tbl.x:
        worst_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        rest_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        # If they are NOT the same, this column likely explains the bad performance
        if not ezr.same(worst_vals, rest_vals):
            important_cols.append(col.txt)
            
    return important_cols

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    factors = blame(header, rows)
    
    print("Analysis: Why do our worst setups leave so many people waiting around?")
    print("The following input factors significantly correlate with poor performance:")
    for factor in factors:
        print(f"- {factor}")
    
    exit(0)
