import ezr

def blame(header, rows):
    """
    Identifies input columns that correlate with 'bad' outcomes (high ydist).
    We compare the distribution of input values in the worst 25% of rows
    against the rest.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the 'worst'
    scored = []
    for r in rows:
        scored.append((ezr.ydist(tbl, r), r))
    
    # Sort by ydist descending (worst first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    n_worst = max(1, len(rows) // 4)
    worst = [x[1] for x in scored[:n_worst]]
    rest = [x[1] for x in scored[n_worst:]]
    
    # For each input column, calculate a 'blame' score
    scores = []
    for col in tbl.x:
        # Get values for worst and rest
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        # Calculate mean difference in normalized space
        # Note: ezr.norm returns a float for Num and the original value for Sym.
        # We must handle Sym columns differently.
        def get_val(col, v):
            res = ezr.norm(col, v)
            return float(res) if isinstance(res, (int, float)) else 0.0

        w_mu = sum(get_val(col, v) for v in w_vals) / len(w_vals)
        r_mu = sum(get_val(col, v) for v in r_vals) / len(r_vals)
        
        # The 'blame' is the magnitude of difference between groups
        scores.append((abs(w_mu - r_mu), col.txt))
    
    # Return top 3 columns that explain the bad performance
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores[:3]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    results = blame(header, rows)
    
    print("Analysis: What factors contribute to short stays (poor goal outcomes)?")
    print("The following input columns are most strongly associated with the worst-performing records:")
    for i, col_name in enumerate(results, 1):
        print(f"{i}. {col_name}")
    
    print("\nThese factors represent the primary differences between the most successful")
    print("and least successful employee records in the dataset.")
