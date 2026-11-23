import csv
from step01 import remember
from step02 import guess

def justify(header, rows, row):
    """
    Estimates the performance of 'row' and compares it against all 'rows'.
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a human-readable explanation.
    """
    # 1. Estimate the goals for the target row
    # We use the guess function from step02, but we need to handle all goals.
    # Since guess only does MRE-, we extend the logic to estimate all goals.
    
    def estimate_row(target_row):
        # Use k-NN (k=5) to estimate all goal columns
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
        
        neighbors = sorted(rows, key=lambda r: dist(r, target_row))[:5]
        estimated = list(target_row)
        for g_idx in goal_indices:
            estimated[g_idx] = sum(n[g_idx] for n in neighbors) / len(neighbors)
        return estimated

    est_row = estimate_row(row)
    
    # 2. Compare against all rows
    # We use the scoring logic from step01 to compare
    all_data = rows + [est_row]
    best_indices = remember(header, all_data)
    
    # Calculate scores for all
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
    
    reason = f"This setup outperforms {p:.1%} of all historical configurations based on its estimated goal metrics."
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
        
        # Test with the last row, masking its goals
        test_row = list(rows[-1])
        for i, h in enumerate(header):
            if h.endswith('-') or h.endswith('+'):
                test_row[i] = "?"
        
        p, reason = justify(header, rows[:-1], test_row)
        print(reason)
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
