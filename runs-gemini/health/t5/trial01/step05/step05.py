import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'bad' as having a high ydist (distance from ideal goals).
    We then compare the distribution of input values in the worst 25% 
    vs the best 25% to find which inputs correlate most with being 'bad'.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (higher is worse)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    
    n = len(sorted_rows) // 4
    best = sorted_rows[:n]
    worst = sorted_rows[-n:]
    
    # For each input column, check if the distribution of values in 'worst'
    # is significantly different from 'best'.
    # We use a simple heuristic: for numeric, compare means; for symbolic, compare modes.
    # We return the names of columns where the 'worst' group deviates most.
    scores = []
    for col in tbl.x:
        # Extract values, ignoring '?'
        b_vals = [r[col.at] for r in best if r[col.at] != "?"]
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        
        if not b_vals or not w_vals:
            continue
            
        if isinstance(col, ezr.Num):
            # Difference in means normalized by standard deviation
            b_mu = sum(b_vals) / len(b_vals)
            w_mu = sum(w_vals) / len(w_vals)
            diff = abs(w_mu - b_mu) / (col.sd + 1e-32)
            scores.append((diff, col.txt))
        else:
            # Difference in frequency of the most common symbol
            b_counts = {}
            for v in b_vals: b_counts[v] = b_counts.get(v, 0) + 1
            w_counts = {}
            for v in w_vals: w_counts[v] = w_counts.get(v, 0) + 1
            
            b_mode = max(b_counts, key=b_counts.get)
            w_mode = max(w_counts, key=w_counts.get)
            
            # Score based on how much the mode frequency shifts
            diff = 1.0 if b_mode != w_mode else 0.0
            scores.append((diff, col.txt))
            
    # Return the top 3 columns that contribute most to the 'badness'
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for score, name in scores[:3]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    culprits = blame(header, rows)
    
    print("Analysis complete: Identifying settings that correlate with poor performance.")
    print("The following input columns are most strongly associated with the worst-performing setups:")
    for i, name in enumerate(culprits):
        print(f"{i+1}. {name}")
    
    exit(0)
