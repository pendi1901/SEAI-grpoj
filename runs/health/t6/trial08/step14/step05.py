import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 25% of rows
    against the rest, identifying columns where the distributions differ 
    significantly using the stats tools from ezr.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the "worst"
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    
    # Split into worst 25% and the rest
    n = len(scored) // 4
    worst = [r for _, r in scored[-n:]]
    rest = [r for _, r in scored[:-n]]
    
    blamed = []
    # Check each input column
    for col in tbl.x:
        # Collect values for this column in both groups
        vals_worst = [r[col.at] for r in worst if r[col.at] != "?"]
        vals_rest = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not vals_worst or not vals_rest:
            continue
            
        # If numeric, check if distributions are different
        if isinstance(col, ezr.Num):
            # If they are NOT the same, the column is a candidate for blame
            if not ezr.same(sorted(vals_worst), sorted(vals_rest)):
                blamed.append(col.txt)
        else:
            # For symbolic, check if the most common value differs significantly
            # or if the distribution of categories is distinct
            if not ezr.same(sorted(vals_worst), sorted(vals_rest)):
                blamed.append(col.txt)
                
    return blamed

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    results = blame(header, rows)
    
    print("Analysis of bad setups complete.")
    print("The following input settings are most strongly associated with poor performance:")
    for name in results:
        print(f" - {name}")
    
    exit(0)
