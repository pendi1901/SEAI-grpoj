import csv
import step05

def blame(header, rows):
    """
    Identifies input columns that have the least impact on performance.
    If a column's distribution in 'bad' rows is statistically similar to 
    its distribution in 'good' rows, it is a candidate for a factory default.
    """
    # Identify goal and input indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Use the logic from step05 to score rows and split into good/bad
    n = len(rows)
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    def normalize(val, vals, reverse=False):
        min_v, max_v = min(vals), max(vals)
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return (1 - norm) if reverse else norm

    scored_rows = []
    for r in rows:
        s = (normalize(r[mre_idx], mres, True) +
             normalize(r[acc_idx], accs, False) +
             normalize(r[pred_idx], preds, False)) / 3
        scored_rows.append((s, r))
    
    scored_rows.sort(key=lambda x: x[0])
    cutoff = max(1, n // 4)
    bad_rows = [x[1] for x in scored_rows[:cutoff]]
    good_rows = [x[1] for x in scored_rows[cutoff:]]
    
    # Calculate difference for each input column
    # Lower difference means the setting doesn't distinguish bad from good
    diffs = []
    for i in input_indices:
        vals_bad = [r[i] for r in bad_rows]
        vals_good = [r[i] for r in good_rows]
        
        if isinstance(vals_bad[0], str):
            # Compare frequency distribution (simple mode check)
            mode_bad = max(set(vals_bad), key=vals_bad.count)
            mode_good = max(set(vals_good), key=vals_good.count)
            d = 0 if mode_bad == mode_good else 1
        else:
            # Compare mean
            d = abs((sum(vals_bad)/len(vals_bad)) - (sum(vals_good)/len(vals_good)))
        
        diffs.append((d, header[i]))
    
    # Sort by difference ascending: smallest difference = safest to leave at default
    diffs.sort(key=lambda x: x[0])
    return [d[1] for d in diffs]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        safe_settings = blame(header, rows)
        print("Settings you can safely leave at factory defaults (least impact on performance):")
        for col in safe_settings[:3]:
            print(f"- {col}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
