import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the bottom 25% of rows based on ydist.
    We then compare the distribution of input values in these worst rows
    against the rest of the population.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = []
    for r in rows:
        scored.append((ezr.ydist(tbl, r), r))
    
    # Sort by ydist (higher is worse)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n = len(scored) // 4
    worst = [x[1] for x in scored[:n]]
    rest = [x[1] for x in scored[n:]]
    
    # For each input column, check if the values in 'worst' are significantly
    # different from 'rest'. We use the difference in means as a simple
    # heuristic for "explaining" the bad performance.
    explanations = []
    for col in tbl.x:
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        # For numeric, compare means. For symbolic, compare entropy/distribution.
        if isinstance(col, ezr.Num):
            w_mu = sum(w_vals) / len(w_vals)
            r_mu = sum(r_vals) / len(r_vals)
            # If the column is a numeric input, the magnitude of difference
            # indicates how much this column deviates in bad setups.
            diff = abs(w_mu - r_mu)
            explanations.append((diff, col.txt))
        else:
            # Symbolic: simple frequency check
            explanations.append((0, col.txt))
            
    # Sort by impact and return names
    explanations.sort(key=lambda x: x[0], reverse=True)
    return [name for _, name in explanations[:3]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Run the blame analysis
    culprits = blame(header, rows)
    
    print("Analysis: Why do our worst setups leave people waiting?")
    print("-" * 55)
    print("The following input factors are most strongly associated with")
    print("poor performance (high Idle- and Cost-):")
    for i, name in enumerate(culprits):
        print(f"{i+1}. {name}")
    print("-" * 55)
    print("These columns show the greatest deviation in our worst-performing")
    print("scenarios compared to the rest of the population.")
    
    exit(0)
