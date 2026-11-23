import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    Uses a threshold based on the 95th percentile of the observed data 
    (or a heuristic if seen is small) to identify a high-performing setup.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Normalize goals: MRE (min), ACC (max), PRED40 (max)
        # Since we don't have global min/max, we use the current 'seen' data
        # to estimate relative quality.
        mre = r[mre_idx]
        acc = r[acc_idx]
        pred = r[pred_idx]
        return (1.0 - mre) + acc + pred

    if not seen:
        return False

    # Calculate scores of all seen rows
    scores = [get_score(r) for r in seen]
    current_score = get_score(row)
    
    # If current row is better than 95% of what we've seen, stop.
    # We use a threshold of 95% of the max score seen so far.
    best_so_far = max(scores)
    
    # Stop if we have seen enough to have a baseline and this is top-tier
    if len(seen) > 20 and current_score >= (0.95 * best_so_far):
        return True
        
    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
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
        print(f"Stopped at row {found_idx + 1}: Found a setup good enough to ship.")
        print(f"Setup details: {rows[found_idx]}")
    else:
        print("Processed all rows without finding a setup meeting the stop criteria.")
