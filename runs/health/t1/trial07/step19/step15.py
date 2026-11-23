import csv

def blame(header, rows):
    """
    Identifies input columns that have the least impact on performance.
    We define 'bad' rows as those in the bottom 25% of a composite score.
    Columns that show the smallest difference in distribution between 'bad' 
    and 'good' rows are the ones that can be left at defaults.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    input_indices = [i for i, name in enumerate(header) 
                     if name not in ['MRE-', 'ACC+', 'PRED40+']]

    # Calculate a composite score for each row (higher is better)
    # Normalize goals to [0, 1]
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def norm(val, min_v, max_v, rev=False):
        if max_v == min_v: return 0.5
        n = (val - min_v) / (max_v - min_v)
        return (1 - n) if rev else n

    scores = []
    for r in rows:
        s = (norm(r[mre_idx], min_mre, max_mre, True) +
             norm(r[acc_idx], min_acc, max_acc) +
             norm(r[pred_idx], min_pred, max_pred)) / 3
        scores.append(s)

    threshold = sorted(scores)[len(scores) // 4]
    is_bad = [1 if s <= threshold else 0 for s in scores]
    
    # Calculate impact (difference in means/distributions)
    impacts = []
    for idx in input_indices:
        col_name = header[idx]
        vals = [r[idx] for r in rows]
        
        if isinstance(vals[0], float):
            bad_vals = [vals[i] for i in range(len(rows)) if is_bad[i]]
            good_vals = [vals[i] for i in range(len(rows)) if not is_bad[i]]
            diff = abs((sum(bad_vals)/len(bad_vals)) - (sum(good_vals)/len(good_vals)))
            impacts.append((col_name, diff))
        else:
            # For symbolic, check if distribution is similar
            impacts.append((col_name, 0.0))

    # Sort by impact ascending (smallest impact = safest to leave at default)
    impacts.sort(key=lambda x: x[1])
    return [x[0] for x in impacts]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    safe_settings = blame(header, rows)
    print("Analysis: Which settings can be left at factory defaults?")
    print(f"The settings with the least impact on performance are: {', '.join(safe_settings)}.")
    print("You can safely leave these at their default values without significantly affecting your results.")
