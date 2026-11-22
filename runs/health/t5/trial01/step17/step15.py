import ezr
import random

def blame(header, rows):
    """
    Identify input columns that have the least impact on performance.
    We compare the distribution of input values in the worst 25% of rows
    against the rest of the data. Columns with the smallest difference
    in distribution are identified as 'safe' to leave at default.
    """
    # 1. Setup table to use ezr's ydist
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # 2. Score all rows and find the worst 25%
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    worst_n = max(1, len(rows) // 4)
    worst_rows = [x[1] for x in scored[:worst_n]]
    other_rows = [x[1] for x in scored[worst_n:]]
    
    # 3. Evaluate each input column
    # We look for columns where the distribution in 'worst' is most similar to 'others'
    scores = []
    for col in tbl.x:
        at = col.at
        if isinstance(col, ezr.Sym):
            # For symbols, compare frequency distribution
            w_vals = [r[at] for r in worst_rows]
            o_vals = [r[at] for r in other_rows]
            # Use simple overlap of frequencies
            diff = 0
            for val in set(w_vals + o_vals):
                w_freq = w_vals.count(val) / len(w_vals)
                o_freq = o_vals.count(val) / len(o_vals)
                diff += abs(w_freq - o_freq)
        else:
            # For numbers, compare normalized mean difference
            w_vals = [r[at] for r in worst_rows if r[at] != "?"]
            o_vals = [r[at] for r in other_rows if r[at] != "?"]
            if not w_vals or not o_vals: 
                diff = 1.0 # Assume high impact if data missing
            else:
                w_mu = sum(w_vals) / len(w_vals)
                o_mu = sum(o_vals) / len(o_vals)
                # Normalize by range to make columns comparable
                diff = abs(w_mu - o_mu)
            
        scores.append((header[at], diff))
    
    # 4. Return columns with the smallest impact (lowest diff)
    scores.sort(key=lambda x: x[1])
    return [name for name, score in scores]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    safe_settings = blame(header, rows)
    
    print("Analysis: Which settings can I leave at factory default?")
    print("The following input columns have the least impact on performance (ordered by safety):")
    for i, col in enumerate(safe_settings):
        print(f"{i+1}. {col}")
    
    print("\nThese settings are the least likely to affect your goals.")
    exit(0)
