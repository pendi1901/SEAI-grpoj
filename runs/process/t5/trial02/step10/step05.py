import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the rows with the highest ydist.
    We compare the distribution of input values in the worst 25% 
    against the best 25% to find the most significant differences.
    """
    # Create a table to handle normalization and ydist
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Score all rows
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist (worst are at the end)
    scored.sort(key=lambda x: x[0])
    
    n = len(scored) // 4
    best = [x[1] for x in scored[:n]]
    worst = [x[1] for x in scored[-n:]]
    
    # Identify input columns (those not ending in + or -)
    input_indices = [i for i, name in enumerate(header) if name[-1] not in "+-"]
    
    # For each input column, check if the distributions differ significantly
    # between best and worst. We use the 'same' function from ezr.
    explanations = []
    for i in input_indices:
        best_vals = [r[i] for r in best if r[i] != "?"]
        worst_vals = [r[i] for r in worst if r[i] != "?"]
        
        if not best_vals or not worst_vals:
            continue
            
        # If they are NOT the same, this column helps explain the difference
        if not ezr.same(best_vals, worst_vals):
            explanations.append(header[i])
            
    return explanations

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    reasons = blame(header, rows)
    
    print("--- Analysis: Why do worst setups have high Idle-? ---")
    print("The following input factors significantly differentiate the worst-performing")
    print("setups from the best-performing ones:")
    for reason in reasons:
        print(f" - {reason}")
    
    print("\nThese factors are the primary drivers of inefficiency in the current process.")
