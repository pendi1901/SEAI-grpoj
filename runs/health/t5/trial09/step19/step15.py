import ezr
import random

def blame(header, rows):
    """
    Identify input columns that are statistically indistinguishable between
    the 'worst' rows and the 'rest' of the rows. If the distribution of a 
    setting is the same in both groups, it implies that changing that 
    setting does not significantly correlate with poor performance.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the "worst" ones
    # Higher ydist means further from the ideal goals (worse performance)
    indexed_rows = []
    for row in rows:
        indexed_rows.append((row, ezr.ydist(tbl, row)))
    
    # Sort by ydist descending (worst first)
    indexed_rows.sort(key=lambda x: x[1], reverse=True)
    
    # Define worst 25%
    split = len(indexed_rows) // 4
    worst = [x[0] for x in indexed_rows[:split]]
    rest = [x[0] for x in indexed_rows[split:]]
    
    safe_to_ignore = []
    
    # Check each input column
    for col in tbl.x:
        at = col.at
        worst_vals = [r[at] for r in worst if r[at] != "?"]
        rest_vals = [r[at] for r in rest if r[at] != "?"]
        
        if not worst_vals or not rest_vals:
            continue
            
        # If the distributions are the same (indistinguishable), 
        # the setting is not a primary driver of poor performance.
        if ezr.same(sorted(worst_vals), sorted(rest_vals), eps=0.35):
            safe_to_ignore.append(header[at])
                
    return safe_to_ignore

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Identify settings that don't contribute to poor performance
    safe_settings = blame(header, rows)
    
    print("Analysis of settings that can be left at default:")
    if safe_settings:
        print("The following settings do not significantly correlate with poor outcomes:")
        for s in safe_settings:
            print(f" - {s}")
    else:
        print("All input settings appear to have a significant impact on performance.")
        
    exit(0)
