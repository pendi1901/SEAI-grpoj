import csv

def flow(header, row, seen):
    """
    Decides whether to stop the run. We stop if the current row is 
    statistically unlikely to be improved upon, based on the 
    diminishing returns of the best observed goals so far.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Normalize goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
        # Since we don't have global min/max, we use the 'seen' data to estimate
        # relative quality.
        mre = r[mre_idx]
        acc = r[acc_idx]
        pred = r[pred_idx]
        return -mre + acc + pred

    if not seen:
        return False

    # Track the best score seen so far
    best_score = max(get_score(s) for s in seen)
    current_score = get_score(row)

    # If we have seen enough data (e.g., 100 rows), check for stagnation.
    # If the current row is significantly better than the best, keep going.
    # If we haven't seen a new 'best' in a long time, stop.
    if len(seen) > 100:
        # Look at the last 100 rows to see if we are still improving
        recent_rows = seen[-100:]
        recent_best = max(get_score(s) for s in recent_rows)
        
        # If the current row is not better than the best of the last 100,
        # and we have a decent sample size, we assume convergence.
        if current_score <= recent_best:
            return True

    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)

        seen = []
        stopped = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Stopping run at index {i}: No significant improvement detected.")
                stopped = True
                break
            seen.append(row)
        
        if not stopped:
            print("Run completed without early stopping.")
        
        exit(0)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        exit(1)
