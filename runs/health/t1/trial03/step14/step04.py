import csv

def flow(header, row, seen):
    """
    Decides whether to accept the current row based on a Pareto-like 
    threshold derived from previously seen data.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # If this is the first row, we have no baseline, so keep looking
    if not seen:
        return False

    # Calculate current row's normalized score relative to history
    mres = [r[mre_idx] for r in seen]
    accs = [r[acc_idx] for r in seen]
    preds = [r[pred_idx] for r in seen]

    min_mre, max_mre = min(mres), max(mres)
    min_acc, max_acc = min(accs), max(accs)
    min_pred, max_pred = min(preds), max(preds)

    def get_score(r):
        s_mre = (max_mre - r[mre_idx]) / (max_mre - min_mre) if max_mre > min_mre else 0
        s_acc = (r[acc_idx] - min_acc) / (max_acc - min_acc) if max_acc > min_acc else 0
        s_pred = (r[pred_idx] - min_pred) / (max_pred - min_pred) if max_pred > min_pred else 0
        return s_mre + s_acc + s_pred

    # Threshold: Accept if the current row is in the top 5% of observed scores
    scores = [get_score(r) for r in seen]
    current_score = get_score(row)
    
    # We define "good enough" as being better than the 95th percentile of seen data
    scores.sort(reverse=True)
    limit = max(1, len(scores) // 20)
    threshold = scores[limit - 1]

    return current_score >= threshold

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    seen = []
    found_idx = -1
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_idx = i
            break
        seen.append(row)

    if found_idx != -1:
        print(f"Stopped at row {found_idx}: Found a setup good enough to ship.")
    else:
        print("No setup met the criteria before the data ended.")
