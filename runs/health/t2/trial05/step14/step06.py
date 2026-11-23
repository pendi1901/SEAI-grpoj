import csv
import step02

def justify(header, rows, row):
    """
    Estimates the performance of 'row' and compares it against all 'rows'.
    Returns (fraction_better, reason_string).
    """
    # 1. Estimate the goals for the target row using k-NN from step02
    # step02.guess returns a list of MRE- predictions for the input rows.
    # We need to estimate all three goals: MRE-, ACC+, PRED40+
    # Since step02 only estimates MRE-, we extend the logic to estimate all 3 goals.
    
    def estimate_all(target_row):
        input_indices = [i for i, name in enumerate(header) if not (name.endswith('-') or name.endswith('+'))]
        
        estimates = []
        for goal_idx in range(3): # MRE-, ACC+, PRED40+
            distances = []
            for tr_row in rows:
                dist = 0.0
                for i in input_indices:
                    if isinstance(target_row[i], str):
                        dist += 0.0 if target_row[i] == tr_row[i] else 1.0
                    else:
                        dist += (target_row[i] - tr_row[i]) ** 2
                distances.append((dist**0.5, tr_row[goal_idx]))
            
            distances.sort(key=lambda x: x[0])
            k = 3
            avg = sum(d[1] for d in distances[:k]) / k
            estimates.append(avg)
        return estimates

    est_mre, est_acc, est_pred = estimate_all(row)
    
    # 2. Scoring logic: lower MRE, higher ACC, higher PRED
    # Normalize goals to [0, 1] to combine them
    mres = [r[0] for r in rows]
    accs = [r[1] for r in rows]
    preds = [r[2] for r in rows]
    
    def norm(val, vals, reverse=False):
        min_v, max_v = min(vals), max(vals)
        if max_v == min_v: return 0.0
        n = (val - min_v) / (max_v - min_v)
        return 1.0 - n if reverse else n

    target_score = norm(est_mre, mres, True) + norm(est_acc, accs) + norm(est_pred, preds)
    
    better_count = 0
    for r in rows:
        r_score = norm(r[0], mres, True) + norm(r[1], accs) + norm(r[2], preds)
        if r_score > target_score:
            better_count += 1
            
    p = 1.0 - (better_count / len(rows))
    reason = f"This setup outperforms {p:.1%} of all known configurations based on its predicted MRE, ACC, and PRED40 metrics."
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        # Test with the last row as a hidden query
        test_row = ["?"] * 3 + rows[-1][3:]
        p, reason = justify(header, rows, test_row)
        
        print(f"Justification: {reason}")
        print(f"Score: {p:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
