import csv

def blame(header, rows):
    """
    Identifies input columns that are 'safe' to leave at factory defaults.
    We define 'safe' as input columns that have low correlation with the 
    performance goals (MRE-, ACC+, PRED40+). If a setting has no significant 
    impact on performance, it can be left at its default.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Normalize goals to a single performance score (higher is better)
    # MRE- (min), ACC+ (max), PRED40+ (max)
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    def norm(val, vals, reverse=False):
        mn, mx = min(vals), max(vals)
        if mx == mn: return 0
        n = (val - mn) / (mx - mn)
        return (1 - n) if reverse else n

    scores = []
    for r in rows:
        s = (norm(r[mre_idx], mres, True) + norm(r[acc_idx], accs) + norm(r[pred_idx], preds))
        scores.append(s)

    # Calculate correlation between each input and the performance score
    # For symbolic, we use a simple variance check or just skip if not numeric
    safe_settings = []
    for i in input_indices:
        col_vals = [r[i] for r in rows]
        if isinstance(col_vals[0], (int, float)):
            # Pearson-like correlation: sum of (x - mean_x) * (y - mean_y)
            mx = sum(col_vals) / len(col_vals)
            my = sum(scores) / len(scores)
            num = sum((col_vals[j] - mx) * (scores[j] - my) for j in range(len(rows)))
            den = (sum((col_vals[j] - mx)**2 for j in range(len(rows))) * 
                   sum((scores[j] - my)**2 for j in range(len(rows))))**0.5
            
            corr = abs(num / den) if den != 0 else 0
            # If correlation is very low, it's safe to leave at default
            if corr < 0.1:
                safe_settings.append(header[i])
        else:
            # For symbolic, check if performance is uniform across categories
            cats = set(col_vals)
            cat_scores = {c: [] for c in cats}
            for j, val in enumerate(col_vals):
                cat_scores[val].append(scores[j])
            
            # If variance between category means is low, it's safe
            means = [sum(cat_scores[c])/len(cat_scores[c]) for c in cats]
            if max(means) - min(means) < 0.1:
                safe_settings.append(header[i])
                
    return safe_settings

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    safe = blame(header, rows)
    print("Settings that can be left at factory defaults without hurting performance:")
    for setting in safe:
        print(f"- {setting}")
    exit(0)
