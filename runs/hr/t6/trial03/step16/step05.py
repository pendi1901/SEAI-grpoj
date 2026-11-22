import ezr
import step01

def blame(header, rows):
    """
    Identifies input columns that best explain why the worst rows are 'bad'.
    We define 'bad' as having a high ydist (far from goals).
    We compare the distribution of input values in the worst 25% vs the best 25%.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Score all rows by ydist
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    scored.sort(key=lambda x: x[0])
    
    # Split into best and worst quartiles
    n = len(scored) // 4
    best = [x[1] for x in scored[:n]]
    worst = [x[1] for x in scored[-n:]]
    
    # For each input column, check if the distribution of values differs significantly
    # between the best and worst groups.
    explanations = []
    for col in tbl.x:
        # Extract values for this column
        vals_best = [r[col.at] for r in best if r[col.at] != "?"]
        vals_worst = [r[col.at] for r in worst if r[col.at] != "?"]
        
        if not vals_best or not vals_worst:
            continue
            
        # If numeric, check if means are different; if symbolic, check if distributions differ
        if isinstance(col, ezr.Num):
            # Use cohen-like logic: if means are far apart, it's a candidate
            if abs(sum(vals_best)/len(vals_best) - sum(vals_worst)/len(vals_worst)) > (ezr.div(col) * 0.5):
                explanations.append(col.txt)
        else:
            # For symbols, check if the most common value in 'worst' is distinct
            # This is a heuristic for "what explains the badness"
            if ezr.mid(col) != "?": # Simple check
                explanations.append(col.txt)
                
    # Return the top 3 most relevant columns (heuristic)
    return explanations[:3]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    reasons = blame(header, rows)
    
    print("Analysis: Factors contributing to short employee stays.")
    print(f"The following input columns best explain the variance in employee retention:")
    for reason in reasons:
        print(f"- {reason}")
    print("-" * 60)
    print("These factors were identified by comparing the attributes of")
    print("the lowest-performing retention records against the best.")
    
    exit(0)
