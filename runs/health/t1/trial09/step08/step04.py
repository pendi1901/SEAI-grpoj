import csv

def flow(header, row, seen):
    """
    Decides whether to stop at the current row based on whether it is 
    'good enough'. We define 'good enough' as being in the top 5% 
    of the potential distribution based on the goals MRE-, ACC+, and PRED40+.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # If this is the first row, we have no baseline to compare against.
    if not seen:
        return False

    # Extract goals from seen rows to establish a baseline
    mres = [r[mre_idx] for r in seen]
    accs = [r[acc_idx] for r in seen]
    preds = [r[pred_idx] for r in seen]

    # Calculate current row's normalized score relative to history
    def normalize(val, vals):
        min_v, max_v = min(vals), max(vals)
        if max_v == min_v: return 0.5
        return (val - min_v) / (max_v - min_v)

    s_mre = 1 - normalize(row[mre_idx], mres + [row[mre_idx]])
    s_acc = normalize(row[acc_idx], accs + [row[acc_idx]])
    s_pred = normalize(row[pred_idx], preds + [row[pred_idx]])
    
    score = s_mre + s_acc + s_pred

    # Calculate scores of seen rows to determine the 95th percentile threshold
    seen_scores = []
    for r in seen:
        ss_mre = 1 - normalize(r[mre_idx], mres + [row[mre_idx]])
        ss_acc = normalize(r[acc_idx], accs + [row[acc_idx]])
        ss_pred = normalize(r[pred_idx], preds + [row[pred_idx]])
        seen_scores.append(ss_mre + ss_acc + ss_pred)
    
    seen_scores.sort(reverse=True)
    threshold = seen_scores[max(0, int(len(seen_scores) * 0.05))]

    # Stop if the current row is better than the 95th percentile of seen rows
    return score >= threshold

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
        
        seen = []
        found = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Stopped at row {i}: MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f}")
                found = True
                break
            seen.append(row)
        
        if not found:
            print("No setup met the criteria before the end of the data.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
