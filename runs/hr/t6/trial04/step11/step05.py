import ezr

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'bad' as having a high ydist. We rank input columns by 
    how much they correlate with the worst 25% of rows.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Score all rows by ydist
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    
    # Split into worst 25% and the rest
    n = len(scored) // 4
    worst = [x[1] for x in scored[-n:]]
    rest = [x[1] for x in scored[:-n]]
    
    # Score each input column by the difference in distribution between worst and rest
    scores = []
    for col in tbl.x:
        if type(col) is ezr.Num:
            w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
            r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
            if w_vals and r_vals:
                w_mu = sum(w_vals) / len(w_vals)
                r_mu = sum(r_vals) / len(r_vals)
                # Score by normalized difference
                diff = abs(w_mu - r_mu) / (ezr.div(col) + 1e-32)
                scores.append((diff, col.txt))
        else:
            # For symbols, use entropy difference
            w_col = ezr.adds([r[col.at] for r in worst if r[col.at] != "?"])
            r_col = ezr.adds([r[col.at] for r in rest if r[col.at] != "?"])
            diff = abs(ezr.div(w_col) - ezr.div(r_col))
            scores.append((diff, col.txt))
            
    # Return the names of the top 3 input columns that explain the badness
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores[:3] if s[0] > 0]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    factors = blame(header, rows)
    
    print("Analysis: What explains short stays (worst performance metrics)?")
    if factors:
        print("The following input columns best explain the worst outcomes:")
        for f in factors:
            print(f" - {f}")
    else:
        print("No input factors clearly explain the worst outcomes.")
