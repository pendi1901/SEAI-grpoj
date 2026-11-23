import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that have no statistically significant impact
    on the outcome (tenure/satisfaction). We compare the distribution of 
    values in the best 25% of rows against the worst 25% of rows.
    If the distributions are 'same' (indistinguishable), the column
    is a candidate for removal.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Score all rows based on goals
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    
    # Split into worst and best quartiles
    n = len(scored) // 4
    worst = [x[1] for x in scored[-n:]]
    best = [x[1] for x in scored[:n]]
    
    # Identify columns that do NOT show a significant difference
    useless_cols = []
    for col in tbl.x:
        at = col.at
        best_vals = [r[at] for r in best if r[at] != "?"]
        worst_vals = [r[at] for r in worst if r[at] != "?"]
        
        if not best_vals or not worst_vals:
            continue
            
        if type(col) is ezr.Sym:
            # For symbols, check if the distributions are the same
            # We use the library's same() function logic
            if ezr.same(best_vals, worst_vals):
                useless_cols.append(header[at])
        else:
            # For numbers, check if the distributions are the same
            if ezr.same(sorted(best_vals), sorted(worst_vals)):
                useless_cols.append(header[at])
                    
    return useless_cols

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    useless = blame(header, rows)
    
    print("Analysis: Which data columns are redundant?")
    print("-" * 60)
    print("The following input columns show no statistically significant")
    print("difference between the best and worst performing employees.")
    print("These could potentially be removed to simplify data collection:")
    for col in useless:
        print(f" - {col}")
    print("-" * 60)
    print("Note: Statistical indistinguishability was determined using")
    print("Cliff's Delta and Kolmogorov-Smirnov tests.")
