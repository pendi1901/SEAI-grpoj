import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected 
    distribution of the goals based on the history seen so far.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # If this is the first row, we can't evaluate it against history
    if not seen:
        return False

    # Collect all seen values for normalization
    mres = [r[mre_idx] for r in seen]
    accs = [r[acc_idx] for r in seen]
    preds = [r[pred_idx] for r in seen]

    # Calculate current row's normalized score relative to history
    def get_norm(val, vals, reverse=False):
        min_v, max_v = min(vals), max(vals)
        if max_v == min_v: return 0.5
        norm = (val - min_v) / (max_v - min_v)
        return (1.0 - norm) if reverse else norm

    score = (get_norm(row[mre_idx], mres, True) +
             get_norm(row[acc_idx], accs, False) +
             get_norm(row[pred_idx], preds, False)) / 3.0

    # Calculate scores of all seen rows
    seen_scores = []
    for r in seen:
        s = (get_norm(r[mre_idx], mres, True) +
             get_norm(r[acc_idx], accs, False) +
             get_norm(r[pred_idx], preds, False)) / 3.0
        seen_scores.append(s)

    # If current score is better than 95% of seen, stop
    threshold = sorted(seen_scores)[int(len(seen_scores) * 0.95)]
    return score >= threshold

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
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
                print(f"Stopped at row {i+1}: Found a configuration that meets the quality threshold.")
                found = True
                break
            seen.append(row)
        
        if not found:
            print("Reached the end of the data without finding a sufficiently high-performing setup.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
