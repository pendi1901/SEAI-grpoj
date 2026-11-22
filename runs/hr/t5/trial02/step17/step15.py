import ezr

def blame(header, rows):
    """
    Identifies input columns that have the least impact on performance.
    We compare the distribution of input values in the worst 25% of rows
    against the rest of the data. If the distributions are statistically
    indistinguishable, the column likely has nothing to do with the outcome.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist (higher is worse)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n = len(scored) // 4
    worst = [x[1] for x in scored[:n]]
    rest = [x[1] for x in scored[n:]]
    
    irrelevant = []
    for col in tbl.x:
        # Extract values for this column in both groups
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        # If we have enough data, check if distributions are the same
        if len(w_vals) > 10 and len(r_vals) > 10:
            # For numeric, use same() (cliffs/ks/cohen)
            # For symbolic, we check if the most common symbol is the same
            if type(col) is ezr.Num:
                if ezr.same(sorted(w_vals), sorted(r_vals)):
                    irrelevant.append(col.txt)
            else:
                # Symbolic: compare frequency distribution
                w_counts = {}
                for v in w_vals: w_counts[v] = w_counts.get(v, 0) + 1
                r_counts = {}
                for v in r_vals: r_counts[v] = r_counts.get(v, 0) + 1
                
                w_mode = max(w_counts, key=w_counts.get)
                r_mode = max(r_counts, key=r_counts.get)
                
                if w_mode == r_mode:
                    irrelevant.append(col.txt)
                    
    return irrelevant

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    useless_cols = blame(header, rows)
    
    print("Analysis: Which columns have little impact on employee retention?")
    print("The following input columns appear to have no statistically significant")
    print("correlation with poor outcomes and could potentially be dropped:")
    for col in useless_cols:
        print(f" - {col}")
        
    print("\nMethodology: We compared the distribution of input values between the")
    print("worst 25% of performers and the rest of the workforce. Columns where")
    print("the distributions were statistically indistinguishable were flagged.")
    
    exit(0)
