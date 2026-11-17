import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 25% of rows
    against the best 25% of rows.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (lower is better)
    scored = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    
    n = len(scored) // 4
    best = scored[:n]
    worst = scored[-n:]
    
    # For each input column, check if the distribution of values differs
    # significantly between the best and worst sets.
    influential = []
    for col in tbl.x:
        b_vals = [r[col.at] for r in best if r[col.at] != "?"]
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        
        if not b_vals or not w_vals:
            continue
            
        # If symbolic, check if the most common value in 'worst' is rare in 'best'
        if isinstance(col, ezr.Sym):
            w_counts = {}
            for v in w_vals: w_counts[v] = w_counts.get(v, 0) + 1
            most_bad = max(w_counts, key=w_counts.get)
            
            b_counts = {}
            for v in b_vals: b_counts[v] = b_counts.get(v, 0) + 1
            if w_counts[most_bad] > (b_counts.get(most_bad, 0) * 2 + 1):
                influential.append(col.txt)
        else:
            # If numeric, check if means are significantly different
            if not ezr.same(b_vals, w_vals, eps=0.5):
                influential.append(col.txt)
                
    return influential

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    results = blame(header, rows)
    
    print("Analysis of settings causing poor performance:")
    if results:
        print("The following settings are strongly associated with the worst-performing setups:")
        for name in results:
            print(f" - {name}")
    else:
        print("No single setting clearly distinguishes the worst setups from the best.")
