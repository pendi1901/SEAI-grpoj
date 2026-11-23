import ezr
import step05

def blame(header, rows):
    """
    Returns a list of input column names that have the least impact on 
    distinguishing the 'worst' rows from the 'rest'.
    
    We reuse the logic from step05 to score columns by their ability to 
    explain 'badness' (high ydist). Columns with the lowest scores 
    are those that have little to do with the performance outcomes.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Score all rows by ydist
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    
    # Split into worst 25% and the rest
    n = len(scored) // 4
    worst = [x[1] for x in scored[-n:]]
    rest = [x[1] for x in scored[:-n]]
    
    # Score each input column by the difference in distribution
    scores = []
    for col in tbl.x:
        if type(col) is ezr.Num:
            w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
            r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
            if w_vals and r_vals:
                w_mu = sum(w_vals) / len(w_vals)
                r_mu = sum(r_vals) / len(r_vals)
                diff = abs(w_mu - r_mu) / (ezr.div(col) + 1e-32)
                scores.append((diff, col.txt))
            else:
                scores.append((0, col.txt))
        else:
            w_col = ezr.adds([r[col.at] for r in worst if r[col.at] != "?"])
            r_col = ezr.adds([r[col.at] for r in rest if r[col.at] != "?"])
            diff = abs(ezr.div(w_col) - ezr.div(r_col))
            scores.append((diff, col.txt))
            
    # Sort by score ascending (least impact first)
    scores.sort(key=lambda x: x[0])
    
    # Return the names of the bottom 5 columns (least explanatory)
    return [s[1] for s in scores[:5]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    useless_factors = blame(header, rows)
    
    print("Analysis: Which columns have little impact on retention metrics?")
    print("The following input columns have the least explanatory power regarding "
          "the worst performance outcomes and could potentially be retired:")
    for f in useless_factors:
        print(f" - {f}")
