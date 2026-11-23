import ezr
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with the worst-performing rows.
    We define 'worst' as the bottom 25% of rows based on ydist.
    We then compare the distribution of each input column in the 'worst'
    set versus the 'best' set. The columns with the largest difference
    in distribution (using standard deviation/mean shifts) are the culprits.
    """
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Score rows to find the worst
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    scored.sort(key=lambda x: x[0])
    
    # Split into worst 25% and best 25%
    n = len(scored) // 4
    worst_rows = [x[1] for x in scored[-n:]]
    best_rows = [x[1] for x in scored[:n]]
    
    # Find input columns (those not ending in - or +)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith("-") or name.endswith("+"))]
    
    # Score inputs by how much they differ between worst and best
    # We use the difference in means (normalized) as a simple heuristic
    scores = []
    for i in input_indices:
        col = tbl.cols[i]
        if isinstance(col, ezr.Num):
            w_vals = [r[i] for r in worst_rows if r[i] != "?"]
            b_vals = [r[i] for r in best_rows if r[i] != "?"]
            if w_vals and b_vals:
                w_mu = sum(w_vals) / len(w_vals)
                b_mu = sum(b_vals) / len(b_vals)
                # We look for large shifts in input values for the worst rows
                scores.append((abs(w_mu - b_mu), header[i]))
    
    # Return the top 3 columns that explain the bad performance
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for score, name in scores[:3]]

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    try:
        header = next(rows_gen)
        rows = list(rows_gen)
        culprits = blame(header, rows)
        print("The worst setups are primarily driven by these input factors:")
        for i, name in enumerate(culprits):
            print(f"{i+1}. {name}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    exit(0)
