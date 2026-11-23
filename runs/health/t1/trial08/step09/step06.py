import csv

def justify(header, rows, row):
    """
    Estimates the performance of 'row' by comparing its inputs to the training data,
    then calculates the fraction of rows it outperforms.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]

    def get_score(r):
        # Normalize: (1 - MRE) + ACC + PRED. Higher is better.
        return (1.0 - r[mre_idx]) + r[acc_idx] + r[pred_idx]

    def distance(r1, r2):
        d = 0
        for i in input_indices:
            v1, v2 = r1[i], r2[i]
            if isinstance(v1, str):
                d += 0 if v1 == v2 else 1
            else:
                d += abs(v1 - v2)
        return d

    # Estimate goals for the target row using 5-nearest neighbors
    distances = sorted([(distance(row, r), r) for r in rows], key=lambda x: x[0])
    k = 5
    neighbors = distances[:k]
    
    # Estimate the target row's goals based on neighbors
    est_mre = sum(n[1][mre_idx] for n in neighbors) / k
    est_acc = sum(n[1][acc_idx] for n in neighbors) / k
    est_pred = sum(n[1][pred_idx] for n in neighbors) / k
    
    est_row = row[:]
    est_row[mre_idx], est_row[acc_idx], est_row[pred_idx] = est_mre, est_acc, est_pred
    
    target_score = get_score(est_row)
    
    # Calculate fraction of rows outperformed
    better_count = sum(1 for r in rows if target_score > get_score(r))
    p = better_count / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all configurations based on its input parameters."
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                processed.append(val if header[i] == 'criterion' else float(val))
            rows.append(processed)
    
    # Test with the last row as a sample
    test_row = rows[-1][:]
    test_row[0], test_row[1], test_row[2] = "?", "?", "?"
    
    p, reason = justify(header, rows, test_row)
    print(f"Justification: {reason}")
