import csv

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with poor performance.
    We define 'bad' as the bottom 25% of rows based on a multi-objective score.
    We then calculate the correlation (or difference in means) between input 
    settings and the 'bad' status.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Score rows to find the worst ones
    def get_score(row):
        # Simple normalization based on min/max of the whole dataset
        mres = [r[mre_idx] for r in rows]
        accs = [r[acc_idx] for r in rows]
        preds = [r[pred_idx] for r in rows]
        
        def norm(v, vals, rev):
            mn, mx = min(vals), max(vals)
            if mx == mn: return 0.5
            n = (v - mn) / (mx - mn)
            return 1.0 - n if rev else n
            
        return (norm(row[mre_idx], mres, True) + 
                norm(row[acc_idx], accs, False) + 
                norm(row[pred_idx], preds, False)) / 3.0

    scored = sorted([(get_score(r), r) for r in rows])
    worst = scored[:len(scored) // 4]
    best = scored[-(len(scored) // 4):]
    
    # Compare mean/distribution of inputs in worst vs best
    impact = []
    for i in input_indices:
        name = header[i]
        w_vals = [r[1][i] for r in worst]
        b_vals = [r[1][i] for r in best]
        
        if isinstance(w_vals[0], str):
            # For symbolic, check frequency difference
            w_freq = w_vals.count(w_vals[0]) / len(w_vals)
            b_freq = b_vals.count(w_vals[0]) / len(b_vals)
            diff = abs(w_freq - b_freq)
        else:
            # For numeric, check difference in means
            diff = abs((sum(w_vals)/len(w_vals)) - (sum(b_vals)/len(b_vals)))
            
        impact.append((diff, name))
    
    impact.sort(reverse=True)
    return [name for _, name in impact[:3]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        culprits = blame(header, rows)
        print("The settings most responsible for poor performance are:")
        for c in culprits:
            print(f"- {c}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
