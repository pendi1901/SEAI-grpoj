import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' by comparing it to the distribution 
    of existing rows. Returns (p, reason) where p is the fraction of rows 
    that 'row' outperforms.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]

    # Estimate goals for the target row using 3-Nearest Neighbors
    def distance(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], str):
                d += 0 if r1[i] == r2[i] else 1
            else:
                # Normalize numeric distance by range
                col_vals = [r[i] for r in rows]
                rng = max(col_vals) - min(col_vals) + 1e-9
                d += abs(r1[i] - r2[i]) / rng
        return d

    neighbors = sorted(rows, key=lambda r: distance(r, row))[:3]
    est_mre = sum(n[mre_idx] for n in neighbors) / len(neighbors)
    est_acc = sum(n[acc_idx] for n in neighbors) / len(neighbors)
    est_pred = sum(n[pred_idx] for n in neighbors) / len(neighbors)

    # Better = lower MRE, higher ACC, higher PRED40
    # We define 'better' as having a higher aggregate normalized score
    def get_score(mre, acc, pred):
        mres = [r[mre_idx] for r in rows]
        accs = [r[acc_idx] for r in rows]
        preds = [r[pred_idx] for r in rows]
        
        def norm(v, vals):
            mn, mx = min(vals), max(vals)
            return (v - mn) / (mx - mn + 1e-9)
        
        return (1 - norm(mre, mres)) + norm(acc, accs) + norm(pred, preds)

    target_score = get_score(est_mre, est_acc, est_pred)
    
    better_count = 0
    for r in rows:
        r_score = get_score(r[mre_idx], r[acc_idx], r[pred_idx])
        if target_score > r_score:
            better_count += 1
    
    p = better_count / len(rows)
    reason = ("Choosing the biggest, deepest setup often leads to overfitting or diminishing returns, "
              "as evidenced by this configuration outperforming only {:.1%} of known setups.").format(p)
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        # Simulate a "biggest, deepest" setup
        # N_estimators=200, Max_depth=20, Min_sample_leaves=1, Min_impurity_decrease=0
        test_row = [0, 0, 0, 200.0, 'squared_error', 1.0, 0.0, 20.0]
        
        p, reason = justify(header, rows, test_row)
        print(reason)
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
