import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that correlate with 'bad' rows.
    'Bad' rows are those with the highest ydist (furthest from ideal).
    We compare the distribution of inputs in the worst 25% of rows
    against the rest of the data.
    """
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows to identify the 'worst'
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
    # from the global mean/median.
    # We look for inputs where the worst rows have significantly different 
    # values than the population.
    scores = []
    for col in input_cols:
        # Get values for this column in worst rows
        vals = [r[col.at] for r in worst_rows if r[col.at] != "?"]
        if not vals:
            continue
            
        # Simple heuristic: difference between mean of worst and global mean
        # normalized by column spread
        global_mid = ezr.mid(col)
        worst_mid = sum(vals) / len(vals) if isinstance(vals[0], (int, float)) else None
        
        if worst_mid is not None:
            diff = abs(worst_mid - global_mid)
            scores.append((diff, col.txt))
            
    # Return names of top 3 columns that explain the bad performance
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in scores[:3]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    rows = list(rows_iter)
    
    reasons = blame(header, rows)
    
    print("Analysis: Why do our worst setups leave people waiting?")
    print("The primary factors contributing to poor performance are:")
    for i, reason in enumerate(reasons, 1):
        print(f"{i}. {reason}")
    
    print("\nThese inputs show the highest deviation in our worst-performing configurations.")
    exit(0)
