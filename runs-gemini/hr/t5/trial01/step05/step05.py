import ezr

def blame(header, rows):
    """
    Identifies input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 25% of rows
    against the rest, returning columns where the distributions differ significantly.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (distance to goals). Higher ydist = worse performance.
    # We define "worst" as the top 25% of rows with the highest ydist.
    scored = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    n_worst = max(1, len(rows) // 4)
    worst = scored[:n_worst]
    rest = scored[n_worst:]
    
    explanations = []
    
    # Check each input column to see if it distinguishes the worst rows
    for col in tbl.x:
        at = col.at
        # Extract values, ignoring "?"
        w_vals = [r[at] for r in worst if r[at] != "?"]
        r_vals = [r[at] for r in rest if r[at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        # If symbolic, check if the most common value in 'worst' is different
        if isinstance(col, ezr.Sym):
            w_mode = max(set(w_vals), key=w_vals.count)
            r_mode = max(set(r_vals), key=r_vals.count)
            if w_mode != r_mode:
                explanations.append(header[at])
        # If numeric, check if distributions are statistically different
        else:
            if not ezr.same(sorted(w_vals), sorted(r_vals)):
                explanations.append(header[at])
                
    return explanations

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Find factors contributing to poor outcomes
    factors = blame(header, rows)
    
    print("Analysis: Factors associated with short stays/poor outcomes.")
    print(f"The following input columns best explain the worst-performing records:")
    for f in factors:
        print(f" - {f}")
    
    print("\nThese factors are statistically distinct in the worst-performing group,")
    print("suggesting they are key drivers of employee attrition or dissatisfaction.")
