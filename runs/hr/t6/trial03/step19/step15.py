import ezr
import step05

def blame(header, rows):
    """
    Identifies input columns that have little to no impact on retention.
    We define 'impact' by checking if the distribution of values in the 
    best 25% of rows is statistically similar to the worst 25% of rows.
    If they are the same, the column is a candidate for removal.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Score all rows by ydist (distance to ideal goals)
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    scored.sort(key=lambda x: x[0])
    
    # Split into best and worst quartiles
    n = len(scored) // 4
    best = [x[1] for x in scored[:n]]
    worst = [x[1] for x in scored[-n:]]
    
    # Identify columns that are NOT statistically different between best and worst
    # These are the columns that have "nothing to do" with retention.
    useless_columns = []
    for col in tbl.x:
        vals_best = [r[col.at] for r in best if r[col.at] != "?"]
        vals_worst = [r[col.at] for r in worst if r[col.at] != "?"]
        
        if not vals_best or not vals_worst:
            continue
            
        # Use ezr.same to check if distributions are indistinguishable
        # If they are the same, the column doesn't differentiate performance
        if ezr.same(vals_best, vals_worst):
            useless_columns.append(col.txt)
            
    return useless_columns

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get columns that don't impact retention
    to_remove = blame(header, rows)
    
    print("Analysis: Which data collection efforts are redundant?")
    print("The following input columns show no statistically significant impact")
    print("on employee retention and could be considered for removal:")
    for col in to_remove:
        print(f"- {col}")
    print("-" * 60)
    print("These columns were identified by comparing the attributes of")
    print("the top-performing employees against the lowest-performing.")
    
    exit(0)
