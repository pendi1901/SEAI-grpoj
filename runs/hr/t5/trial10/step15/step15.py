import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goals.
    We define 'bad' as having a high ydist (far from ideal goals).
    We compare the distribution of values in the worst 25% of rows 
    against the best 25% of rows for each input column.
    Columns where the distributions are statistically indistinguishable 
    are candidates for removal.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows and sort them
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0])
    
    n = len(scored) // 4
    best = [x[1] for x in scored[:n]]
    worst = [x[1] for x in scored[-n:]]
    
    # We look for input columns where the distribution of values does NOT 
    # differ significantly between the best and worst rows.
    useless_columns = []
    
    for col in tbl.x:
        # Collect values for this column
        best_vals = [r[col.at] for r in best if r[col.at] != "?"]
        worst_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        
        if not best_vals or not worst_vals:
            continue
            
        # Check if the distributions are statistically the same
        # If they are the same, the column doesn't help distinguish 
        # between good and bad outcomes.
        if ezr.same(best_vals, worst_vals):
            useless_columns.append(col.txt)
                
    return useless_columns

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the columns that have little to no impact on performance
    unimportant_factors = blame(header, rows)
    
    print("Analysis: Which data columns are redundant?")
    print("The following input columns show no significant correlation with performance outcomes:")
    if unimportant_factors:
        for factor in unimportant_factors:
            print(f"- {factor}")
        print("\nRecommendation: These columns can be removed to reduce data collection overhead.")
    else:
        print("All input columns appear to have some correlation with performance outcomes.")
        
    exit(0)
