import csv
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate with poor performance.
    We define 'bad' rows as the bottom 25% based on the score from step01.
    We then compare the distribution of input values in 'bad' rows vs 'good' rows.
    """
    # Identify goal and input indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Calculate scores for all rows to identify the worst performers
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
    for i, r in enumerate(rows):
        s = (normalize(r[mre_idx], mres, True) +
             normalize(r[acc_idx], accs, False) +
             normalize(r[pred_idx], preds, False)) / 3
        scored_rows.append((s, r))
    
    # Sort by score ascending to find the bottom 25%
    scored_rows.sort(key=lambda x: x[0])
    cutoff = max(1, n // 4)
    bad_rows = [x[1] for x in scored_rows[:cutoff]]
    good_rows = [x[1] for x in scored_rows[cutoff:]]
    
    # For each input column, check if the mean/mode in bad_rows differs from good_rows
    # We look for columns where the bad rows have a distinct value distribution
    def get_diff(idx):
        vals_bad = [r[idx] for r in bad_rows]
        vals_good = [r[idx] for r in good_rows]
        if isinstance(vals_bad[0], str):
            # Compare mode
            mode_bad = max(set(vals_bad), key=vals_bad.count)
            mode_good = max(set(vals_good), key=vals_good.count)
            return 1 if mode_bad != mode_good else 0
        else:
            # Compare mean
            return abs((sum(vals_bad)/len(vals_bad)) - (sum(vals_good)/len(vals_good)))

    diffs = []
    for i in input_indices:
        diffs.append((get_diff(i), header[i]))
    
    # Return the top 2 columns that contribute most to the difference
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
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        blamed = blame(header, rows)
        print("The settings most responsible for poor performance are:")
        for col in blamed:
            print(f"- {col}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
