import ezr
import random

def blame(header, rows):
    """
    Identify input columns that are NOT statistically different between 
    the worst-performing rows and the rest of the data. 
    If a column's distribution is the same in both groups, it implies 
    that the setting does not influence poor performance, meaning it 
    can be left at factory defaults.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Rank rows by ydist (lower is better, so higher ydist is 'bad')
    scored = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    
    # Split into worst 25% and the rest
    n_worst = len(rows) // 4
    worst = scored[:n_worst]
    rest = scored[n_worst:]
    
    safe_to_default = []
    
    # Check each input column
    for col in tbl.x:
        at = col.at
        # Extract values for this column
        vals_worst = [r[at] for r in worst if r[at] != "?"]
        vals_rest = [r[at] for r in rest if r[at] != "?"]
        
        if not vals_worst or not vals_rest:
            continue
            
        # If the distributions are NOT significantly different, 
        # the column is likely not causing the poor performance.
        if ezr.same(vals_worst, vals_rest):
            safe_to_default.append(header[at])
            
    return safe_to_default

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    safe_settings = blame(header, rows)
    
    print("Optimization Analysis: Which settings can be left at factory defaults?")
    if safe_settings:
        print("The following input settings show no significant difference between "
              "the worst-performing setups and the rest of the data:")
        for s in safe_settings:
            print(f" - {s}")
        print("\nYou can likely leave these at their default values without impacting performance.")
    else:
        print("All input settings appear to influence performance significantly.")
    
    exit(0)
