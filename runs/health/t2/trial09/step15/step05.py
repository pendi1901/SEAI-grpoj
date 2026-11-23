import csv
from step01 import remember

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with 'bad' performance.
    'Bad' is defined as the bottom 10% of rows based on the composite score.
    We compare the distribution of each input column in the 'bad' set 
    against the 'good' set (top 10%).
    """
    # Identify goals and inputs
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]

    # Score all rows to find the bottom 10%
    # We reuse remember logic by inverting the score or just sorting
    # Let's get the scores for all rows
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(row):
        # Normalize logic from step01
        mres = [r[mre_idx] for r in rows]
        accs = [r[acc_idx] for r in rows]
        preds = [r[pred_idx] for r in rows]
        
        def norm(v, vals, rev):
            mn, mx = min(vals), max(vals)
            if mx == mn: return 0.5
            n = (v - mn) / (mx - mn)
            return 1 - n if rev else n
            
        return (norm(row[mre_idx], mres, True) + 
                norm(row[acc_idx], accs, False) + 
                norm(row[pred_idx], preds, False)) / 3

    scored_rows = sorted([(get_score(r), r) for r in rows], key=lambda x: x[0])
    
    n = len(scored_rows) // 10
    bad_rows = [x[1] for x in scored_rows[:n]]
    good_rows = [x[1] for x in scored_rows[-n:]]

    # For each input, calculate the difference in means between bad and good
    diffs = []
    for i in input_indices:
        if isinstance(bad_rows[0][i], str):
            # Symbolic: difference in frequency of the most common value in bad rows
            vals = [r[i] for r in bad_rows]
            mode = max(set(vals), key=vals.count)
            bad_freq = vals.count(mode) / len(vals)
            good_freq = [r[i] for r in good_rows].count(mode) / len(good_rows)
            diffs.append((abs(bad_freq - good_freq), header[i]))
        else:
            # Numeric: difference in means
            bad_mean = sum(r[i] for r in bad_rows) / len(bad_rows)
            good_mean = sum(r[i] for r in good_rows) / len(good_rows)
            diffs.append((abs(bad_mean - good_mean), header[i]))

    # Return the top 2 columns that differentiate bad from good
    diffs.sort(key=lambda x: x[0], reverse=True)
    return [d[1] for d in diffs[:2]]

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

    blame_cols = blame(header, rows)
    print("The settings most responsible for poor performance are:")
    for col in blame_cols:
        print(f"- {col}")
