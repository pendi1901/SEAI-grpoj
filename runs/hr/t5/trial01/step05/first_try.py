import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that correlate with 'bad' outcomes (high ydist).
    We compare the distribution of input values in the worst 25% of rows
    against the rest, using the difference in means/modes as a proxy for 'blame'.
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
    # Score = difference in normalized distance to the goal
    scores = []
    for col in tbl.x:
        # Get values for worst and rest
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        # Calculate mean difference in normalized space
        w_mu = sum(ezr.norm(col, v) for v in w_vals) / len(w_vals)
        r_mu = sum(ezr.norm(col, v) for v in r_vals) / len(r_vals)
        
        # The 'blame' is how much the worst group deviates from the rest
        # towards the 'bad' direction (away from goal)
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
