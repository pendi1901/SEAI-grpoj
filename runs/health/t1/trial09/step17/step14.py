import csv

def flow(header, row, seen):
    """
    Returns True if the current row is 'good enough' to stop the process.
    We define 'good enough' as being in the top 5% of the distribution 
    of all rows seen so far, based on a multi-objective score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # If we haven't seen enough data, keep going
    if len(seen) < 20:
        return False

    # Collect all data to normalize
    all_rows = seen + [row]
    mres = [r[mre_idx] for r in all_rows]
    accs = [r[acc_idx] for r in all_rows]
    preds = [r[pred_idx] for r in all_rows]

    def normalize(val, vals):
        min_v, max_v = min(vals), max(vals)
        if max_v == min_v: return 0.5
        return (val - min_v) / (max_v - min_v)

    # Calculate score for the current row
    s_mre = 1 - normalize(row[mre_idx], mres)
    s_acc = normalize(row[acc_idx], accs)
    s_pred = normalize(row[pred_idx], preds)
    current_score = s_mre + s_acc + s_pred

    # Calculate scores for all seen rows
    seen_scores = []
    for r in seen:
        ss_mre = 1 - normalize(r[mre_idx], mres)
        ss_acc = normalize(r[acc_idx], accs)
        ss_pred = normalize(r[pred_idx], preds)
        seen_scores.append(ss_mre + ss_acc + ss_pred)
    
    seen_scores.sort(reverse=True)
    
    # Stop if current row is better than the 95th percentile of seen rows
    threshold_idx = max(0, int(len(seen_scores) * 0.05))
    threshold = seen_scores[threshold_idx]
    
    return current_score >= threshold

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
        stopped = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Stopping run at row {i+1}: Found a high-performing configuration.")
                print(f"MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f}")
                stopped = True
                break
            seen.append(row)
        
        if not stopped:
            print("Processed all rows without finding a significant improvement.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
