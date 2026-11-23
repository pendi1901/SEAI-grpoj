import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the bottom 25% of rows by ydist.
    We then compare the distribution of inputs in the worst rows vs the rest.
    """
    # Create a table to handle normalization and ydist
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows
    scored = []
    for r in rows:
        scored.append((ezr.ydist(tbl, r), r))
    
    # Sort by ydist (higher is worse)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n_worst = len(rows) // 4
    worst = [x[1] for x in scored[:n_worst]]
    rest = [x[1] for x in scored[n_worst:]]
    
    # Find input columns (those not ending in - or +)
    input_indices = [i for i, name in enumerate(header) 
                     if not name.endswith(('-', '+'))]
    
    # Score columns by how much their distribution differs between worst and rest
    # We use a simple difference in means for numeric columns
    scores = []
    for i in input_indices:
        col = tbl.cols[i]
        if isinstance(col, ezr.Num):
            w_vals = [r[i] for r in worst if r[i] != "?"]
            r_vals = [r[i] for r in rest if r[i] != "?"]
            if w_vals and r_vals:
                w_mu = sum(w_vals) / len(w_vals)
                r_mu = sum(r_vals) / len(r_vals)
                scores.append((abs(w_mu - r_mu), header[i]))
    
    # Return the top 3 columns that explain the difference
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for score, name in scores[:3]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Run the blame analysis
    culprits = blame(header, rows)
    
    print("Analysis: Why do our worst setups leave people waiting around?")
    print("The primary drivers for poor performance (high idle time/cost) are:")
    for i, name in enumerate(culprits, 1):
        print(f"{i}. {name}")
    print("\nThese input factors show the strongest correlation with the worst-performing setups.")
    
    exit(0)
