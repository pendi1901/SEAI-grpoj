import csv
import step01
import step07

def choose(header, rows, label):
    """
    Finds a setup that is both high-performing and 'small'.
    'Small' is defined as having a low N_estimators value.
    We sample 50 rows, label them, and select the one that balances
    high performance (composite score) with low N_estimators.
    """
    n = len(rows)
    # Sample 50 rows evenly to get a representative spread
    step = n // 50
    indices = [i * step for i in range(50)]
    
    labeled_data = []
    for i in indices:
        goals = label(i)
        row = list(rows[i])
        for j, h in enumerate(header):
            if h.endswith('-') or h.endswith('+'):
                row[j] = goals[j]
        labeled_data.append((i, row))
    
    # Identify indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    n_idx = header.index('N_estimators')
    
    # Normalize goals
    mres = [r[1][mre_idx] for r in labeled_data]
    accs = [r[1][acc_idx] for r in labeled_data]
    preds = [r[1][pred_idx] for r in labeled_data]
    n_vals = [r[1][n_idx] for r in labeled_data]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)
    min_n, max_n = min(n_vals), max(n_vals)
    
    def norm(val, lo, hi, rev=False):
        if hi == lo: return 0.5
        n = (val - lo) / (hi - lo)
        return 1 - n if rev else n

    best_idx = -1
    best_score = -1.0
    
    for i, row in labeled_data:
        s1 = norm(row[mre_idx], min_mre, max_mre, True)
        s2 = norm(row[acc_idx], min_acc, max_acc)
        s3 = norm(row[pred_idx], min_pred, max_pred)
        # Performance score
        perf = (s1 + s2 + s3) / 3
        # Size score (minimize N_estimators)
        size = norm(row[n_idx], min_n, max_n, True)
        
        # Combined score: prioritize performance, but penalize large size
        total = (perf * 0.7) + (size * 0.3)
        
        if total > best_score:
            best_score = total
            best_idx = i
            
    return best_idx

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                # Mask goals
                for i, h in enumerate(header):
                    if h.endswith('-') or h.endswith('+'):
                        processed[i] = "?"
                rows.append(processed)
        
        true_data = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                true_data.append([float(val) if header[i] not in ['criterion'] else val 
                                  for i, val in enumerate(row)])
        
        def label(i):
            row = true_data[i]
            return [row[j] for j, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        
        best_idx = choose(header, rows, label)
        print(f"Recommended setup for nightly runs: Row index {best_idx}.")
        print("This setup balances high forecast accuracy with a small model size.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
