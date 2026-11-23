import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the bottom 10% of rows by ydist.
    We then compare the distribution of inputs in the worst rows vs the rest.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Score all rows
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending (worst first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 10% and the rest
    n = len(rows) // 10
    worst = [x[1] for x in scored[:n]]
    rest = [x[1] for x in scored[n:]]
    
    # For each input column, check if the distribution in 'worst' is 
    # significantly different from 'rest' using the stats in ezr.
    # We look for columns where the values are 'not same'.
    explanations = []
    for col in tbl.x:
        xs = [r[col.at] for r in worst if r[col.at] != "?"]
        ys = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not ezr.same(xs, ys):
            explanations.append(col.txt)
            
    return explanations

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    factors = blame(header, rows)
    
    print("Analysis: Why do our worst setups leave so many people waiting around?")
    print("The following input factors significantly correlate with poor performance:")
    for f in factors:
        print(f" - {f}")
    
    exit(0)
