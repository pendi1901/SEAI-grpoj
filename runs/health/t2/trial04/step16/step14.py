import csv
import step01

def flow(header, row, seen):
    """
    Decides whether to stop the process by checking if the current row
    is significantly better than the best seen so far.
    We stop if the current row is in the top 1% of all seen rows.
    """
    if not seen:
        return False

    # Identify goal indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Combine seen rows with current to normalize
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

    # Calculate scores for all seen rows and the current one
    current_score = get_score(row, all_rows)
    seen_scores = [get_score(r, all_rows) for r in seen]
    
    # Stop if current row is better than 99% of previous bests
    # or if it is the absolute best seen so far and we have enough history
    if len(seen) > 50 and current_score > max(seen_scores):
        return True
        
    return False

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
    stopped_at = -1
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            stopped_at = i
            break
        seen.append(row)

    if stopped_at != -1:
        print(f"Optimization stopped at run {stopped_at}. The performance has plateaued.")
    else:
        print("Optimization completed all runs without finding a significant improvement plateau.")
