import ezr
import step05

def blame(header, rows):
    """
    Identifies input columns that have nothing to do with tenure.
    We define 'nothing to do' as columns where the distribution of values
    is statistically indistinguishable between the 'best' and 'worst' 
    performing employees.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (worst first)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    
    # Define worst and best sets (top/bottom 20%)
    n = max(1, len(rows) // 5)
    worst = sorted_rows[:n]
    best = sorted_rows[-n:]
    
    # Identify columns that are NOT significant (i.e., 'same' returns True)
    irrelevant = []
    for col in tbl.x:
        xs = [r[col.at] for r in worst if r[col.at] != "?"]
        ys = [r[col.at] for r in best if r[col.at] != "?"]
        
        if len(xs) > 1 and len(ys) > 1:
            # If distributions are the same, this column does not explain the difference
            if ezr.same(xs, ys):
                irrelevant.append(col.txt)
                
    return irrelevant

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    useless_factors = blame(header, rows)
    
    print("Analysis of data collection efficiency:")
    if useless_factors:
        print("The following input columns show no significant correlation with tenure "
              "and could potentially be removed from future data collection:")
        for f in useless_factors:
            print(f" - {f}")
    else:
        print("All input columns show some statistical correlation with tenure.")
    
    exit(0)
