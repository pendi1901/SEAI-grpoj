import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that have no statistically significant impact on 
    the goal outcomes. We compare the distribution of values in the 'best' 
    rows vs the 'worst' rows. If the distributions are the same, the column 
    likely has nothing to do with the outcome.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to rank them
    # Lower ydist is better.
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist ascending (best to worst)
    scored.sort(key=lambda x: x[0])
    
    n = len(rows)
    # Compare the top 25% (best) vs bottom 25% (worst)
    best = [x[1] for x in scored[:n // 4]]
    worst = [x[1] for x in scored[n // 4:]]
    
    # Identify input columns (not goals)
    input_cols = [c for c in tbl.x]
    
    # If the distributions of a column are the same in best and worst,
    # it implies the column does not distinguish performance.
    irrelevant = []
    for col in input_cols:
        at = col.at
        b_vals = [r[at] for r in best if r[at] != "?"]
        w_vals = [r[at] for r in worst if r[at] != "?"]
        
        if not b_vals or not w_vals:
            continue
            
        # If the distributions are indistinguishable, it's a candidate for removal
        if ezr.same(sorted(b_vals), sorted(w_vals)):
            irrelevant.append(header[at])
            
    return irrelevant

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    results = blame(header, rows)
    
    print("Analysis: Which columns have no impact on how long people stay?")
    print("The following input columns show no statistically significant difference")
    print("between the best-performing rows and the rest of the population:")
    if results:
        for col in results:
            print(f"  - {col}")
    else:
        print("  None. All columns appear to have some impact.")
    
    exit(0)
