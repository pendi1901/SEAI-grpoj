import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'bad' as having a high ydist (far from goals).
    We compare the distribution of values in the worst 25% of rows 
    against the best 25% of rows for each input column.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (distance to ideal goals)
    # Higher ydist means worse performance
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    
    n = len(sorted_rows) // 4
    best = sorted_rows[:n]
    worst = sorted_rows[-n:]
    
    scores = []
    for col in tbl.x:
        # Extract values for this column from best and worst groups
        b_vals = [r[col.at] for r in best if r[col.at] != "?"]
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        
        if not b_vals or not w_vals:
            continue
            
        # If distributions are significantly different (not same), 
        # this column is a candidate for explaining the difference.
        if not ezr.same(b_vals, w_vals):
            # Simple heuristic: difference in means
            b_mid = ezr.mid(ezr.adds(b_vals))
            w_mid = ezr.mid(ezr.adds(w_vals))
            
            # For numeric, use absolute difference; for symbolic, use 1 if different
            diff = abs(b_mid - w_mid) if isinstance(b_mid, (int, float)) else (1 if b_mid != w_mid else 0)
            scores.append((header[col.at], diff))
            
    # Return names of columns with the highest impact
    scores.sort(key=lambda x: x[1], reverse=True)
    return [name for name, score in scores[:3]]

if __name__ == "__main__":
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    factors = blame(header, rows)
    
    print("Analysis: What factors contribute to short stays?")
    print(f"The primary input columns associated with poor retention are: {', '.join(factors)}.")
    print("These factors show the most significant divergence between high-retention and low-retention employees.")
