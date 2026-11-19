import csv
import step01
import step02

def justify(header, rows, row):
    """
    Estimates the performance of 'row' and compares it to 'rows'.
    Returns (p, reason) where p is the fraction of rows worse than 'row'.
    """
    # 1. Estimate the goals for the target row
    # We use the k-NN approach from step02 to fill in the "?" goals
    # We need to prepare the row correctly for step02.guess
    test_row = [row[i] if i > 0 else "?" for i in range(len(row))]
    estimated_mre = step02.guess(header, rows, [test_row])[0]
    
    # For simplicity in this context, we estimate other goals as the mean of the dataset
    # as they are not explicitly handled by step02's guess function
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    est_acc = sum(r[acc_idx] for r in rows) / len(rows)
    est_pred = sum(r[pred_idx] for r in rows) / len(rows)
    
    # 2. Score the target row
    mre_idx, acc_idx, pred_idx = 0, 1, 2
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.0
        norm = (val - min_v) / (max_v - min_v)
        return (1.0 - norm) if reverse else norm

    def get_score(m, a, p):
        return (normalize(m, min(mres), max(mres), True) +
                normalize(a, min(accs), max(accs), False) +
                normalize(p, min(preds), max(preds), False)) / 3.0

    target_score = get_score(estimated_mre, est_acc, est_pred)
    
    # 3. Compare against all rows
    scores = [get_score(r[mre_idx], r[acc_idx], r[pred_idx]) for r in rows]
    better_than = [s for s in scores if target_score > s]
    p = len(better_than) / len(rows)
    
    reason = f"This setup is estimated to outperform {p:.1%} of all configurations based on its multi-objective score."
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed.append(float(val))
                    else:
                        processed.append(val)
                rows.append(processed)
        
        # Test with the first row as the target
        target = [ "?" for _ in range(len(header))]
        target[3:] = rows[0][3:]
        
        p, reason = justify(header, rows, target)
        print(f"Performance Rank: {p:.4f}")
        print(f"Justification: {reason}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
