import csv

def flow(header, row, seen):
    """
    Decides whether to stop at the current row.
    We stop if the current row's utility is significantly better than 
    the best utility seen so far, or if we have seen enough data to 
    conclude that further improvements are unlikely (diminishing returns).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_utility(r):
        # Utility: -MRE + ACC + PRED40
        # We assume goals are normalized or comparable in scale
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    if not seen:
        return False

    current_utility = get_utility(row)
    seen_utilities = [get_utility(r) for r in seen]
    best_seen = max(seen_utilities)

    # Stop if we have seen at least 50 rows and the current row is 
    # not improving upon the best seen by a significant margin.
    # This acts as an early stopping criterion for optimization.
    if len(seen) > 50:
        # If the current row is better than the best seen, we take it.
        if current_utility > best_seen:
            return True
        
        # If we have seen many rows without improvement, stop to save costs.
        # Here we check if the best has not improved in the last 50 rows.
        recent_best = max(seen_utilities[-50:])
        if best_seen > recent_best + 0.1: # Threshold for "improvement"
            return False
        else:
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
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Optimization stopped at row {i+1} as no further significant improvement is expected.")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("Processed all rows; no early stopping criteria met.")
