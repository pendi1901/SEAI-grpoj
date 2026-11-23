import csv

def flow(header, row, seen):
    """
    Decides whether to stop based on whether the current row is a 'plateau' 
    or a 'peak' relative to the history. We stop if the current row's 
    performance is significantly worse than the best seen so far, 
    indicating that we have likely passed the optimal point.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Normalize: (1 - MRE) + ACC + PRED. Higher is better.
        return (1.0 - r[mre_idx]) + r[acc_idx] + r[pred_idx]

    if not seen:
        return False

    current_score = get_score(row)
    best_score = max(get_score(r) for r in seen)
    
    # If we haven't seen an improvement in a while, or if the current 
    # performance is significantly lower than the best, we stop.
    # Here, we stop if the current score is less than 90% of the best score
    # after at least 50 rows have been processed.
    if len(seen) > 50 and current_score < (0.9 * best_score):
        return True
        
    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                processed.append(val if header[i] == 'criterion' else float(val))
            rows.append(processed)

    seen = []
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopping criteria met at row {i + 1}.")
            print("The best setup has likely been found; further runs are unlikely to improve results.")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("Processed all rows; no significant plateau detected.")
