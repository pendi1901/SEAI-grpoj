import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance.
    We define 'bad' as the bottom 25% of rows based on the composite score.
    We then compare the distribution of input values in 'bad' rows 
    vs 'good' rows to find features with the largest divergence.
    """
    # Use step01 logic to score rows
    n = len(rows)
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def normalize(val, min_v, max_v, reverse=False):
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return 1 - norm if reverse else norm

    scored = []
    for row in rows:
        s = (normalize(row[mre_idx], min_mre, max_mre, True) +
             normalize(row[acc_idx], min_acc, max_acc) +
             normalize(row[pred_idx], min_pred, max_pred)) / 3
        scored.append((s, row))
    
    scored.sort(key=lambda x: x[0])
    
    # Bottom 25% are 'bad', top 25% are 'good'
    q = n // 4
    bad = [x[1] for x in scored[:q]]
    good = [x[1] for x in scored[-q:]]
    
    input_cols = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Simple heuristic: find input columns where the mean/mode differs most
    diffs = []
    for i in input_cols:
        if isinstance(bad[0][i], float):
            bad_val = sum(r[i] for r in bad) / len(bad)
            good_val = sum(r[i] for r in good) / len(good)
            diffs.append((abs(bad_val - good_val), header[i]))
        else:
            # For symbolic, compare frequency of the most common value
            bad_mode = max(set(r[i] for r in bad), key=[r[i] for r in bad].count)
            good_mode = max(set(r[i] for r in good), key=[r[i] for r in good].count)
            diffs.append((1 if bad_mode != good_mode else 0, header[i]))
            
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [d[1] for d in diffs[:2]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        culprits = blame(header, rows)
        print("The settings most responsible for poor performance are:")
        for c in culprits:
            print(f"- {c}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
