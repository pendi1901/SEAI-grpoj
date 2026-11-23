import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' using k-Nearest Neighbors and compares
    it to the population to answer why 'biggest/deepest' isn't always best.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]

    # Normalize goals for scoring
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    def norm(val, min_v, max_v, rev=False):
        if max_v == min_v: return 0.5
        n = (val - min_v) / (max_v - min_v)
        return (1 - n) if rev else n

    def get_score(r):
        return (norm(r[mre_idx], min(mres), max(mres), True) +
                norm(r[acc_idx], min(accs), max(accs)) +
                norm(r[pred_idx], min(preds), max(preds))) / 3

    # Estimate goals for the input row using k-NN
    def distance(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], str):
                d += 0 if r1[i] == r2[i] else 1
            else:
                # Normalize numeric distance
                col_vals = [r[i] for r in rows]
                d += abs(r1[i] - r2[i]) / (max(col_vals) - min(col_vals) + 1e-9)
        return d

    distances = sorted([(distance(row, r), r) for r in rows], key=lambda x: x[0])
    k = 10
    neighbors = distances[:k]
    
    est_mre = sum(n[1][mre_idx] for n in neighbors) / k
    est_acc = sum(n[1][acc_idx] for n in neighbors) / k
    est_pred = sum(n[1][pred_idx] for n in neighbors) / k
    
    est_row = list(row)
    est_row[mre_idx], est_row[acc_idx], est_row[pred_idx] = est_mre, est_acc, est_pred
    
    my_score = get_score(est_row)
    all_scores = [get_score(r) for r in rows]
    better_than = sum(1 for s in all_scores if my_score > s)
    p = better_than / len(rows)
    
    reason = "Using the largest, deepest setup often leads to overfitting or diminishing returns, as evidenced by this configuration outperforming only {:.1%} of the observed experimental space.".format(p * 100)
    return (p, reason)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth'] else val for i, val in enumerate(row)]
            rows.append(processed)
    
    # Test with a "biggest/deepest" setup
    test_row = [0, 0, 0, 200.0, 'squared_error', 1.0, 1.0, 20.0]
    p, reason = justify(header, rows, test_row)
    print(reason)
