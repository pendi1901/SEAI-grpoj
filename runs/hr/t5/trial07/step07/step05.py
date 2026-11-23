import ezr

def blame(header, rows):
    """
    Identifies input columns that best explain why the worst rows are bad.
    We define 'bad' as having a high ydist (distance from ideal goals).
    We compare the distribution of values in the worst 25% of rows against
    the rest, looking for columns where the values differ significantly.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending to get the 'worst' rows
    scored.sort(key=lambda x: x[0], reverse=True)
    
    n = len(rows)
    worst = [x[1] for x in scored[:n // 4]]
    rest = [x[1] for x in scored[n // 4:]]
    
    # Identify input columns (not goals)
    input_cols = [c for c in tbl.x]
    
    explanations = []
    for col in input_cols:
        at = col.at
        # Collect values for this column
        w_vals = [r[at] for r in worst if r[at] != "?"]
        r_vals = [r[at] for r in rest if r[at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        # If the distributions are significantly different, this column explains the badness
        if not ezr.same(sorted(w_vals), sorted(r_vals)):
            explanations.append(header[at])
            
    return explanations

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    results = blame(header, rows)
    
    print("Analysis: What factors contribute to short stays (worst performance)?")
    print("The following input columns show a statistically significant difference")
    print("between the worst-performing rows and the rest of the population:")
    for col in results:
        print(f"  - {col}")
    
    exit(0)
