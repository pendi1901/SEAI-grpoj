import csv

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance.
    We define 'bad' rows as those in the bottom 25% of the aggregate score.
    We then compare the distribution of input values in 'bad' rows vs 'good' rows.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]

    # Calculate aggregate scores
    mres = [r[mre_idx] for r in rows]
    accs = [r[acc_idx] for r in rows]
    preds = [r[pred_idx] for r in rows]
    
    def norm(v, vals):
        mn, mx = min(vals), max(vals)
        return (v - mn) / (mx - mn) if mx > mn else 0.5

    scores = []
    for r in rows:
        s = (1 - norm(r[mre_idx], mres)) + norm(r[acc_idx], accs) + norm(r[pred_idx], preds)
        scores.append(s)

    # Split into bottom 25% (bad) and top 25% (good)
    combined = sorted(zip(scores, rows), key=lambda x: x[0])
    n = len(combined)
    bad = [x[1] for x in combined[:n // 4]]
    good = [x[1] for x in combined[3 * n // 4:]]

    # Find inputs where the mean/mode in 'bad' differs most from 'good'
    diffs = []
    for i in input_indices:
        name = header[i]
        if isinstance(bad[0][i], float):
            bad_val = sum(r[i] for r in bad) / len(bad)
            good_val = sum(r[i] for r in good) / len(good)
            diff = abs(bad_val - good_val)
        else:
            # For symbolic, compare frequency of the most common value
            bad_vals = [r[i] for r in bad]
            good_vals = [r[i] for r in good]
            mode_bad = max(set(bad_vals), key=bad_vals.count)
            diff = abs(bad_vals.count(mode_bad) / len(bad_vals) - 
                       good_vals.count(mode_bad) / len(good_vals))
        diffs.append((diff, name))

    # Return top 2 inputs that contribute most to the difference
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [d[1] for d in diffs[:2]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        culprits = blame(header, rows)
        print("The settings most responsible for poor performance are:")
        for c in culprits:
            print(f"- {c}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
