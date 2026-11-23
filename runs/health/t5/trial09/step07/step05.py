import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 25% of rows
    against the rest of the data. Columns where the distributions differ
    significantly (using the statistical tests in ezr) are flagged as 'blameworthy'.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the "worst" ones
    # Higher ydist means further from the ideal goals
    indexed_rows = []
    for i, row in enumerate(rows):
        indexed_rows.append((row, ezr.ydist(tbl, row)))
    
    # Sort by ydist descending (worst first)
    indexed_rows.sort(key=lambda x: x[1], reverse=True)
    
    # Define worst 25%
    split = len(indexed_rows) // 4
    worst = [x[0] for x in indexed_rows[:split]]
    rest = [x[0] for x in indexed_rows[split:]]
    
    blame_list = []
    
    # Check each input column
    for col in tbl.x:
        at = col.at
        # Extract values for this column
        worst_vals = [r[at] for r in worst if r[at] != "?"]
        rest_vals = [r[at] for r in rest if r[at] != "?"]
        
        if not worst_vals or not rest_vals:
            continue
            
        # If the column is numeric, use statistical tests to see if distributions differ
        if isinstance(col, ezr.Num):
            # If they are NOT the same, the column distribution in the worst rows
            # is significantly different from the rest, implying it contributes to the badness.
            if not ezr.same(sorted(worst_vals), sorted(rest_vals), eps=0.35):
                blame_list.append(header[at])
        else:
            # For symbolic columns, check if the most frequent value differs significantly
            # or if the distribution of symbols is skewed in the worst set.
            # A simple heuristic: if the top symbol in 'worst' is different from 'rest'
            # or the counts are heavily imbalanced.
            w_counts = {v: worst_vals.count(v) for v in set(worst_vals)}
            r_counts = {v: rest_vals.count(v) for v in set(rest_vals)}
            
            w_top = max(w_counts, key=w_counts.get)
            r_top = max(r_counts, key=r_counts.get)
            
            if w_top != r_top:
                blame_list.append(header[at])
                
    return blame_list

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    culprits = blame(header, rows)
    
    print("Analysis of settings contributing to poor performance:")
    if culprits:
        print("The following settings appear to be driving poor outcomes:")
        for c in culprits:
            print(f" - {c}")
    else:
        print("No specific settings were identified as primary drivers of poor performance.")
        
    exit(0)
