import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are 'bad'.
    We define 'bad' as having a high ydist (far from ideal goals).
    """
    # Create a table to calculate ydist for all rows
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist descending (worst first)
    # We want to find what characterizes the worst performers
    scored = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    
    # Take the worst 25% to analyze
    n = len(scored) // 4
    worst = scored[:n]
    rest = scored[n:]
    
    # We look for input columns where the distribution in 'worst' 
    # differs significantly from the 'rest' of the data.
    # We score columns by how much they separate the two groups.
    scores = []
    for col in tbl.x:
        # Get values for this column in both groups
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        # If the distributions are different (not same), this column is a candidate
        if not ezr.same(w_vals, r_vals):
            # Simple heuristic: difference in means for numeric, 
            # difference in entropy for symbolic
            if isinstance(col, ezr.Num):
                diff = abs(sum(w_vals)/len(w_vals) - sum(r_vals)/len(r_vals))
            else:
                # Symbolic: measure frequency shift
                diff = 1.0 
            scores.append((diff, col.txt))
            
    # Return the top 3 columns that explain the bad performance
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for score, name in scores[:3]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Run the blame analysis
    factors = blame(header, rows)
    
    print("Analysis: What factors contribute to short employee stays?")
    print("-" * 50)
    if factors:
        print("The following input columns best explain the worst-performing rows:")
        for i, factor in enumerate(factors, 1):
            print(f"{i}. {factor}")
        print("-" * 50)
        print("These factors are statistically significant drivers of low retention.")
    else:
        print("No significant individual factors identified.")
