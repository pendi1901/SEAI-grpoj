import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the bottom 25% of rows by ydist.
    We then compare the distribution of input values in these worst rows
    against the rest of the data to find which inputs correlate with high ydist.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = [(ezr.ydist(tbl, r), r) for r in rows]
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n_worst = len(rows) // 4
    worst = [x[1] for x in scored[:n_worst]]
    rest = [x[1] for x in scored[n_worst:]]
    
    # For each input column, check if the distribution in 'worst'
    # is significantly different from 'rest' using ezr's statistical tests.
    # We look for columns where the values are 'different' (not same).
    significant_inputs = []
    for col in tbl.x:
        xs = [r[col.at] for r in worst if r[col.at] != "?"]
        ys = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if len(xs) > 1 and len(ys) > 1:
            # If they are NOT the same, this column helps explain the difference
            if not ezr.same(xs, ys):
                significant_inputs.append(header[col.at])
                
    return significant_inputs

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Get the columns that explain the worst performance
    factors = blame(header, rows)
    
    print("Analysis: Why do our worst setups leave so many people waiting around?")
    print("The following input factors are statistically linked to poor performance:")
    for factor in factors:
        print(f"- {factor}")
        
    exit(0)
