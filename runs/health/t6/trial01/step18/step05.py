import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 10% of rows
    against the rest of the data.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((ezr.ydist(tbl, row), i))
    
    # Sort by ydist descending (worst rows first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Define worst 10%
    limit = max(1, len(rows) // 10)
    worst_indices = {x[1] for x in scored[:limit]}
    
    worst_rows = [rows[i] for i in worst_indices]
    best_rows = [rows[i] for i in range(len(rows)) if i not in worst_indices]
    
    # For each input column, check if the distribution in 'worst' is 
    # significantly different from 'best' using the stats tools.
    # We look for columns where the values in 'worst' are 'different' 
    # from 'best'.
    suspects = []
    for col in tbl.x:
        at = col.at
        worst_vals = [r[at] for r in worst_rows if r[at] != "?"]
        best_vals = [r[at] for r in best_rows if r[at] != "?"]
        
        if not worst_vals or not best_vals:
            continue
            
        # If symbolic, compare frequency distributions
        if isinstance(col, ezr.Sym):
            # Simple heuristic: if the most common value in worst is 
            # different from the most common in best
            w_counts = {}
            for v in worst_vals: w_counts[v] = w_counts.get(v, 0) + 1
            b_counts = {}
            for v in best_vals: b_counts[v] = b_counts.get(v, 0) + 1
            
            w_mode = max(w_counts, key=w_counts.get)
            b_mode = max(b_counts, key=b_counts.get)
            if w_mode != b_mode:
                suspects.append(header[at])
        else:
            # If numeric, use the stats tests
            if not ezr.same(sorted(worst_vals), sorted(best_vals)):
                suspects.append(header[at])
                
    return suspects

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    suspects = blame(header, rows)
    
    print("Analysis of bad setups:")
    print("The following settings appear to contribute most to poor performance:")
    for s in suspects:
        print(f"- {s}")
    
    if not suspects:
        print("No specific settings were identified as primary drivers of poor performance.")
