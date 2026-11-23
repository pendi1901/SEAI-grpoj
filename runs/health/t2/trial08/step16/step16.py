import csv
from step01 import remember
from step02 import guess as original_guess

def justify(header, rows, row):
    """
    Estimates the goals for 'row' and compares it against all 'rows'.
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a one-sentence explanation of why bigger/deeper isn't always better.
    """
    # 1. Estimate goals for the target row using k-NN (k=5)
    # We use the guess logic from step02, extended to all goals
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            if isinstance(r1[i], str):
                d += 0 if r1[i] == r2[i] else 1
            else:
                d += abs(r1[i] - r2[i])
        return d
    
    neighbors = sorted(rows, key=lambda r: dist(r, row))[:5]
    est_row = list(row)
    for g_idx in goal_indices:
        est_row[g_idx] = sum(n[g_idx] for n in neighbors) / len(neighbors)
    
    # 2. Score all rows (including estimated row)
    all_data = rows + [est_row]
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    def get_score(r):
        mres = [x[mre_idx] for x in all_data]
        accs = [x[acc_idx] for x in all_data]
        preds = [x[pred_idx] for x in all_data]
        
        def norm(v, vals, rev=False):
            mn, mx = min(vals), max(vals)
            if mx == mn: return 0.0
            n = (v - mn) / (mx - mn)
            return (1.0 - n) if rev else n
            
        return (norm(r[mre_idx], mres, True) + norm(r[acc_idx], accs) + norm(r[pred_idx], preds)) / 3.0

    target_score = get_score(est_row)
    better_count = sum(1 for r in rows if get_score(r) < target_score)
    p = better_count / len(rows)
    
    reason = "Bigger and deeper configurations often lead to overfitting, which degrades performance compared to more balanced, moderate settings."
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])
        
        # Create a "big/deep" test row
        test_row = [0.0, 0.0, 0.0, 200.0, 'squared_error', 1.0, 0.0, 20.0]
        for i, h in enumerate(header):
            if h.endswith('-') or h.endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows, test_row)
        print(f"Fraction of configurations outperformed: {p:.4f}")
        print(f"Analysis: {reason}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
