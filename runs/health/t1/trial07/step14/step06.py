import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' using k-Nearest Neighbors,
    then calculates the percentile rank against the provided 'rows'.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]

    def get_score(r):
        # Normalize goals: MRE (min), ACC (max), PRED40 (max)
        # We use the min/max from the dataset to normalize
        mres = [x[mre_idx] for x in rows]
        accs = [x[acc_idx] for x in rows]
        preds = [x[pred_idx] for x in rows]
        
        def norm(val, min_v, max_v, rev=False):
            if max_v == min_v: return 0.5
            n = (val - min_v) / (max_v - min_v)
            return (1 - n) if rev else n

        s = (norm(r[mre_idx], min(mres), max(mres), True) +
             norm(r[acc_idx], min(accs), max(accs)) +
             norm(r[pred_idx], min(preds), max(preds))) / 3
        return s

    # Estimate goals for the input row using k-NN
    def distance(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], str):
                d += 0 if r1[i] == r2[i] else 1
            else:
                d += abs(r1[i] - r2[i])
        return d

    distances = sorted([(distance(row, r), r) for r in rows], key=lambda x: x[0])
    k = 5
    neighbors = distances[:k]
    
    # Estimate goals
    est_mre = sum(n[1][mre_idx] for n in neighbors) / k
    est_acc = sum(n[1][acc_idx] for n in neighbors) / k
    est_pred = sum(n[1][pred_idx] for n in neighbors) / k
    
    est_row = list(row)
    est_row[mre_idx], est_row[acc_idx], est_row[pred_idx] = est_mre, est_acc, est_pred
    
    # Compare against all rows
    my_score = get_score(est_row)
    all_scores = [get_score(r) for r in rows]
    better_than = sum(1 for s in all_scores if my_score > s)
    p = better_than / len(rows)
    
    reason = f"This configuration is estimated to outperform {p:.1%} of all known setups based on its similarity to high-performing neighbors."
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
    
    # Test with a sample row
    test_row = [0, 0, 0, 150.0, 'squared_error', 5.0, 5.0, 5.0]
    p, reason = justify(header, rows, test_row)
    print(f"Score: {p:.4f}")
    print(f"Reason: {reason}")
