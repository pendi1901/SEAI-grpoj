import csv

def flow(header, row, seen):
    """
    Decides whether to stop the run based on whether the current row 
    is a significant improvement over the best seen so far.
    We use a 'plateau' detection strategy: if we haven't seen a 
    significant improvement in a while, we stop.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Normalize goals: MRE (min), ACC (max), PRED40 (max)
        # Since we don't have global min/max, we use the current row's 
        # values relative to the 'seen' population.
        if not seen:
            return 0
        
        mres = [s[mre_idx] for s in seen]
        accs = [s[acc_idx] for s in seen]
        preds = [s[pred_idx] for s in seen]
        
        def norm(val, vals, rev=False):
            min_v, max_v = min(vals), max(vals)
            if max_v == min_v: return 0.5
            n = (val - min_v) / (max_v - min_v)
            return (1 - n) if rev else n

        return (norm(r[mre_idx], mres, True) +
                norm(r[acc_idx], accs) +
                norm(r[pred_idx], preds)) / 3

    if not seen:
        return False

    current_score = get_score(row)
    best_score = max(get_score(s) for s in seen)

    # If we have seen at least 50 rows and the current row is not 
    # significantly better than the best seen (e.g., within 5% improvement),
    # we assume we have hit a plateau and stop.
    if len(seen) > 50:
        if current_score <= best_score * 1.05:
            # Check if we've been stagnant for a while
            recent_scores = [get_score(s) for s in seen[-20:]]
            if max(recent_scores) <= best_score * 1.01:
                return True

    return False

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth'] else val for i, val in enumerate(row)]
            rows.append(processed)

    seen = []
    stopped_at = -1
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            stopped_at = i
            break
        seen.append(row)

    if stopped_at != -1:
        print(f"Optimization stopped at run {stopped_at}.")
        print("The best configuration has plateaued; further runs are unlikely to yield significant improvements.")
    else:
        print("Optimization completed all runs without hitting a clear plateau.")
