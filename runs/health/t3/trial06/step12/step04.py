import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the performance 
    distribution observed so far, based on a normalized utility score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Utility = (1 - MRE) + ACC + PRED
        # Since we don't have global min/max, we use the current row's 
        # values relative to the 'seen' history.
        mre = r[mre_idx]
        acc = r[acc_idx]
        pred = r[pred_idx]
        return (1.0 - mre) + acc + pred

    if not seen:
        return False

    current_score = get_score(row)
    seen_scores = [get_score(r) for r in seen]
    
    # Threshold: Is this row better than 95% of what we have seen?
    # We require at least 20 rows to have a meaningful distribution.
    if len(seen) < 20:
        return False
    
    seen_scores.sort(reverse=True)
    # Top 5% index
    threshold_idx = max(0, int(len(seen_scores) * 0.05))
    threshold_score = seen_scores[threshold_idx]
    
    return current_score >= threshold_score

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    seen = []
    found_idx = -1
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_idx = i
            break
        seen.append(row)

    if found_idx != -1:
        print(f"Stopped at row {found_idx + 1} (1-indexed).")
        print(f"Setup: MRE={rows[found_idx][0]:.4f}, ACC={rows[found_idx][1]:.4f}, PRED40={rows[found_idx][2]:.4f}")
    else:
        print("No setup met the 'good enough' criteria before the end of the data.")
