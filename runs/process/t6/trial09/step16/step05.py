import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the bottom 25% of rows by ydist.
    We compare the distribution of input values in the worst rows 
    against the rest of the data.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the worst
    scored = []
    for r in rows:
        scored.append((ezr.ydist(tbl, r), r))
    
    # Sort by ydist descending (worst first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    n_worst = max(1, len(rows) // 4)
    worst_rows = [x[1] for x in scored[:n_worst]]
    best_rows = [x[1] for x in scored[n_worst:]]
    
    # For each input column, check if the distribution in 'worst' 
    # is significantly different from 'best' using ezr.same.
    # If they are different, the column is a candidate for 'blame'.
    blame_cols = []
    for col in tbl.x:
        worst_vals = [r[col.at] for r in worst_rows if r[col.at] != "?"]
        best_vals = [r[col.at] for r in best_rows if r[col.at] != "?"]
        
        if not ezr.same(worst_vals, best_vals):
            blame_cols.append(col.txt)
            
    return blame_cols

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    blamed = blame(header, rows)
    
    print("Analysis: Why do our worst setups leave so many people waiting around?")
    print("The following input factors significantly correlate with poor performance:")
    for col in blamed:
        print(f"- {col}")
    
    exit(0)
