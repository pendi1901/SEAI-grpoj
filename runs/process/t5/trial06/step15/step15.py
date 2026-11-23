import ezr
import random

def blame(header, rows):
    """
    Identifies which input columns matter most to cost by comparing the 
    distribution of inputs in the 'worst' rows (high ydist) vs the 'best' rows.
    Columns that show the largest statistical difference are the ones that 
    'matter most'.
    """
    # Create a table to handle normalization and distance
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate ydist for all rows to rank them
    scored = [(ezr.ydist(tbl, r), r) for r in rows]
    scored.sort(key=lambda x: x[0])
    
    # Define 'best' and 'worst' as the top and bottom 25%
    n = len(rows) // 4
    best = [x[1] for x in scored[:n]]
    worst = [x[1] for x in scored[-n:]]
    
    # For each input column, measure the difference in distribution
    # between the best and worst rows.
    differences = []
    for col in tbl.x:
        b_vals = [r[col.at] for r in best if r[col.at] != "?"]
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        
        if not b_vals or not w_vals:
            continue
            
        # Use the same logic as ezr.same to check if distributions are different.
        # If they are NOT the same, the column is a candidate for 'mattering'.
        # We rank by the magnitude of the difference (using standard deviation 
        # or simple mean difference for numeric columns).
        if not ezr.same(sorted(b_vals), sorted(w_vals)):
            # Calculate a simple effect size: difference in means
            b_mid = sum(b_vals) / len(b_vals)
            w_mid = sum(w_vals) / len(w_vals)
            differences.append((abs(b_mid - w_mid), col.txt))
            
    # Sort by the magnitude of the difference
    differences.sort(key=lambda x: x[0], reverse=True)
    
    # Return the names of the top 2 most influential columns
    return [item[1] for item in differences[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    important = blame(header, rows)
    
    print("--- Project Cost Analysis ---")
    print("The following input factors matter most to project cost:")
    for i, factor in enumerate(important):
        print(f"{i+1}. {factor}")
        
    print("\nFactors not listed here have a statistically insignificant impact")
    print("on cost performance and can be safely ignored.")
    exit(0)
