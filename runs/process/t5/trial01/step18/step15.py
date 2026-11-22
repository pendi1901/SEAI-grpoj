import ezr
import random

def blame(header, rows):
    """
    Identifies the most important input columns by comparing the 
    distribution of inputs in the worst 25% of rows against the rest.
    The columns with the highest 'impact' (difference in means/distribution)
    are the ones that matter most to cost.
    """
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows to identify the 'worst'
    # ydist measures how far a row's goals are from the best possible
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending (worst first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Define worst 25%
    n_worst = max(1, len(rows) // 4)
    worst_rows = [x[1] for x in scored[:n_worst]]
    
    # Identify input columns (exclude goals)
    input_cols = [c for c in tbl.x]
    
    # Score columns by how much their values in 'worst' rows deviate 
    # from the global mean.
    scores = []
    for col in input_cols:
        # Get values for this column in worst rows
        vals = [r[col.at] for r in worst_rows if r[col.at] != "?"]
        if not vals:
            continue
            
        # For numeric columns, use the difference in means.
        # For symbolic columns, use the difference in entropy/distribution.
        if isinstance(col, ezr.Num):
            global_mid = ezr.mid(col)
            worst_mid = sum(vals) / len(vals)
            diff = abs(worst_mid - global_mid)
        else:
            # For symbols, we check how much the most common symbol in 
            # the worst rows differs from the global most common.
            global_mid = ezr.mid(col)
            worst_counts = {}
            for v in vals: worst_counts[v] = worst_counts.get(v, 0) + 1
            worst_mid = max(worst_counts, key=worst_counts.get)
            diff = 1.0 if worst_mid != global_mid else 0.0
            
        scores.append((diff, col.txt))
            
    # Return names of columns that explain the bad performance
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in scores]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    factors = blame(header, rows)
    
    print("Analysis: What matters most to project cost?")
    print(f"Most influential factors: {factors[0]} and {factors[1]}.")
    print(f"Factors you can safely stop worrying about: {factors[-1]}.")
    print("\nThese rankings are based on how much each input deviates in our worst-performing configurations.")
    
    exit(0)
