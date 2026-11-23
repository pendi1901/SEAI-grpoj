import csv

def justify(header, rows, row):
    """
    Estimates the performance of a 'big, deep' setup and compares it to the 
    rest of the data to see if 'bigger' actually means 'better'.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Identify input columns
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]

    def get_score(r):
        # Normalize: (1 - MRE) + ACC + PRED. Higher is better.
        return (1.0 - r[mre_idx]) + r[acc_idx] + r[pred_idx]

    # Estimate goals for the target row using 5-nearest neighbors
    def distance(r1, r2):
        d = 0
        for i in input_indices:
            v1, v2 = r1[i], r2[i]
            if isinstance(v1, str):
                d += 0 if v1 == v2 else 1
            else:
                d += abs(v1 - v2)
        return d

    distances = sorted([(distance(row, r), r) for r in rows], key=lambda x: x[0])
    k = 5
    neighbors = distances[:k]
    
    est_mre = sum(n[1][mre_idx] for n in neighbors) / k
    est_acc = sum(n[1][acc_idx] for n in neighbors) / k
    est_pred = sum(n[1][pred_idx] for n in neighbors) / k
    
    est_row = row[:]
    est_row[mre_idx], est_row[acc_idx], est_row[pred_idx] = est_mre, est_acc, est_pred
    
    target_score = get_score(est_row)
    
    # Calculate fraction of rows outperformed
    better_count = sum(1 for r in rows if target_score > get_score(r))
    p = better_count / len(rows)
    
    reason = "Bigger, deeper setups often lead to overfitting or diminishing returns, meaning they do not necessarily outperform simpler configurations."
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
    
    # Create a "big, deep" setup: Max N_estimators and Max_depth
    n_est_idx = header.index('N_estimators')
    max_d_idx = header.index('Max_depth')
    
    test_row = [0.0] * len(header)
    for i in range(len(header)):
        if i == n_est_idx: test_row[i] = 200.0
        elif i == max_d_idx: test_row[i] = 20.0
        elif header[i] == 'criterion': test_row[i] = 'squared_error'
        elif header[i] in ['MRE-', 'ACC+', 'PRED40+']: test_row[i] = "?"
        else: test_row[i] = 1.0
        
    p, reason = justify(header, rows, test_row)
    print(f"Analysis: {reason}")
    print(f"This 'big' setup is estimated to outperform {p:.2f} of all configurations.")
