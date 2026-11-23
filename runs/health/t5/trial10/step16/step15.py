import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 10% of rows
    against the rest of the data. Columns with little difference are
    candidates for factory defaults.
    """
    # Create a table to handle column roles and normalization
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the worst ones
    # Higher ydist means worse performance
    scored = []
    for i, row in enumerate(rows):
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending to get the worst rows
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Take the worst 10%
    limit = max(1, int(len(rows) * 0.1))
    worst_rows = [x[1] for x in scored[:limit]]
    other_rows = [x[1] for x in scored[limit:]]
    
    # For each input column, calculate the difference in distribution
    # between the worst rows and the rest.
    scores = []
    for col in tbl.x:
        at = col.at
        # Extract values for this column
        worst_vals = [r[at] for r in worst_rows if r[at] != "?"]
        other_vals = [r[at] for r in other_rows if r[at] != "?"]
        
        if not worst_vals or not other_vals:
            continue
            
        # For numeric columns, compare means. For symbolic, compare mode frequency.
        if isinstance(col, ezr.Num):
            mu_w = sum(worst_vals) / len(worst_vals)
            mu_o = sum(other_vals) / len(other_vals)
            diff = abs(mu_w - mu_o)
        else:
            # Difference in probability of the most common symbol
            w_counts = {v: worst_vals.count(v) for v in set(worst_vals)}
            o_counts = {v: other_vals.count(v) for v in set(other_vals)}
            w_mode = max(w_counts, key=w_counts.get)
            diff = abs((w_counts.get(w_mode, 0)/len(worst_vals)) - 
                       (o_counts.get(w_mode, 0)/len(other_vals)))
            
        scores.append((diff, header[at]))
    
    # Sort by difference ascending: the smallest difference means the column
    # does not differentiate the worst rows from the rest, making it a 
    # candidate for a factory default.
    scores.sort(key=lambda x: x[0])
    return [name for _, name in scores]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        data = list(ezr.csv(filename))
        header = data[0]
        rows = data[1:]
        
        results = blame(header, rows)
        
        print("Analysis: Which settings can be left at factory defaults?")
        print("The following input columns have the least impact on performance,")
        print("making them the best candidates for fixed factory defaults:")
        for i, col in enumerate(results):
            print(f"{i+1}. {col}")
            
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
