import csv
from step05 import blame as original_blame

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with 'bad' performance.
    The customer wants to know which settings can be left at factory defaults 
    without hurting anything; these are the settings that have the least 
    impact on performance (i.e., the lowest 'damage' scores).
    """
    # We reuse the logic from step05 which calculates the 'damage' (impact)
    # of each input column on performance.
    # The columns with the lowest damage are the ones that can be left at defaults.
    
    # Identify input columns
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate damage for all input columns
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    def get_score(row):
        mres = [r[mre_idx] for r in rows]
        accs = [r[acc_idx] for r in rows]
        preds = [r[pred_idx] for r in rows]
        def norm(v, vals):
            mn, mx = min(vals), max(vals)
            return (v - mn) / (mx - mn) if mx > mn else 0
        return (1 - norm(row[mre_idx], mres)) + norm(row[acc_idx], accs) + norm(row[pred_idx], preds)

    scored_rows = sorted([(get_score(r), r) for r in rows], key=lambda x: x[0])
    n = len(scored_rows)
    worst = [r for _, r in scored_rows[:n // 4]]
    best = [r for _, r in scored_rows[-n // 4:]]
    
    damages = []
    for i in input_indices:
        if isinstance(worst[0][i], str):
            w_val = max(set(r[i] for r in worst), key=lambda x: [r[i] for r in worst].count(x))
            b_val = max(set(r[i] for r in best), key=lambda x: [r[i] for r in best].count(x))
            diff = 1.0 if w_val != b_val else 0.0
        else:
            w_avg = sum(r[i] for r in worst) / len(worst)
            b_avg = sum(r[i] for r in best) / len(best)
            diff = abs(w_avg - b_avg)
        damages.append((diff, header[i]))
    
    # Sort by damage ascending: lowest damage = safest to leave at default
    damages.sort(key=lambda x: x[0])
    
    return [name for _, name in damages]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)
            
    safe_settings = blame(header, rows)
    print("Settings you can safely leave at factory defaults (least impact on performance):")
    for name in safe_settings:
        print(f" - {name}")
