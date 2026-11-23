import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the rows with the highest ydist.
    We compare the distribution of input values in the worst 20% 
    against the rest, looking for features that correlate with high ydist.
    """
    # Create table to calculate ydist
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending to get the worst rows
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 20% and the rest
    n_worst = max(1, len(rows) // 5)
    worst = [x[1] for x in scored[:n_worst]]
    rest = [x[1] for x in scored[n_worst:]]
    
    # For each input column, check if the distribution of values in 'worst'
    # is significantly different from 'rest' using the same() statistical test.
    # If they are different, the column is a candidate for 'blame'.
    blamed = []
    for col in tbl.x:
        at = col.at
        # Extract values for this column
        vals_worst = [r[at] for r in worst if r[at] != "?"]
        vals_rest = [r[at] for r in rest if r[at] != "?"]
        
        if not vals_worst or not vals_rest:
            continue
            
        # If they are NOT the same, this column contributes to the difference
        if not ezr.same(vals_worst, vals_rest):
            blamed.append(header[at])
            
    return blamed

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the columns to blame
    blame_cols = blame(header, rows)
    
    # Identify all input columns
    all_inputs = [h for h in header if h[-1] not in "+-"]
    
    # Determine what can be safely ignored (inputs not in the blame list)
    safe_to_ignore = [col for col in all_inputs if col not in blame_cols]
    
    print("Analysis: Which project factors matter most to cost?")
    print("The following input factors are statistically linked to poor performance:")
    for col in blame_cols:
        print(f" - {col}")
    
    print("\nYou can safely stop worrying about these factors:")
    for col in safe_to_ignore:
        print(f" - {col}")
