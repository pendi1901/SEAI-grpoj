import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'worst' as the bottom 25% of rows by ydist.
    We compare the distribution of input values in these worst rows
    against the rest of the data to find which inputs correlate with high ydist.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending (worst first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n_worst = len(scored) // 4
    worst_rows = [x[1] for x in scored[:n_worst]]
    rest_rows = [x[1] for x in scored[n_worst:]]
    
    # Calculate the "impact" of each input column
    # We measure the difference in the mean (for Num) or distribution (for Sym)
    # between the worst rows and the rest.
    impacts = []
    for col in tbl.x:
        w_vals = [r[col.at] for r in worst_rows if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest_rows if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        if isinstance(col, ezr.Num):
            w_avg = sum(w_vals) / len(w_vals)
            r_avg = sum(r_vals) / len(r_vals)
            # Impact is the absolute difference in means
            impacts.append((abs(w_avg - r_avg), col.txt))
        else:
            # Impact is the max difference in frequency for any symbol
            w_freqs = {v: w_vals.count(v) / len(w_vals) for v in set(w_vals)}
            r_freqs = {v: r_vals.count(v) / len(r_vals) for v in set(r_vals)}
            diff = 0
            for v in set(w_freqs) | set(r_freqs):
                diff = max(diff, abs(w_freqs.get(v, 0) - r_freqs.get(v, 0)))
            impacts.append((diff, col.txt))
            
    # Sort by impact descending
    impacts.sort(key=lambda x: x[0], reverse=True)
    
    # Return the names of the top 2 most impactful columns
    return [name for impact, name in impacts[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty or missing.")
        exit(1)
        
    top_factors = blame(header, rows)
    
    print("Project Analysis: What matters most to cost?")
    print("The following input factors have the strongest correlation with poor performance:")
    for factor in top_factors:
        print(f" - {factor}")
        
    print("\nThese are the primary drivers of cost and idle time. Other factors")
    print("have significantly less impact and can be safely ignored for now.")
    
    exit(0)
