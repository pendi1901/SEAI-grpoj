import csv
import step01

def flow(header, row, seen):
    """
    Decides whether to accept the current row based on whether it is 
    better than any previously seen row.
    
    A row is better if it dominates or performs better on the weighted 
    average of normalized objectives (MRE-, ACC+, PRED40+).
    """
    if not seen:
        return True

    # Identify indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Combine current row with seen rows to normalize
    all_rows = seen + [row]
    
    def get_score(r, rows_data):
        mres = [x[mre_idx] for x in rows_data]
        accs = [x[acc_idx] for x in rows_data]
        preds = [x[pred_idx] for x in rows_data]
        
        def norm(val, vals, reverse=False):
            min_v, max_v = min(vals), max(vals)
            if max_v == min_v: return 0.5
            n = (val - min_v) / (max_v - min_v)
            return 1.0 - n if reverse else n
        
        s1 = norm(r[mre_idx], mres, reverse=True)
        s2 = norm(r[acc_idx], accs)
        s3 = norm(r[pred_idx], preds)
        return (s1 + s2 + s3) / 3.0

    # If current row is the best seen so far, accept it
    current_score = get_score(row, all_rows)
    seen_scores = [get_score(r, all_rows) for r in seen]
    
    return current_score >= max(seen_scores)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)

    seen = []
    accepted = None
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            accepted = (i, row)
            break
        seen.append(row)

    if accepted:
        idx, row = accepted
        print(f"Stopped at row {idx} (0-indexed).")
        print(f"Accepted setup: MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f}")
    else:
        print("No suitable setup found.")
