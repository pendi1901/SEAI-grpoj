import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the potential 
    distribution based on the goals: MRE- (min), ACC+ (max), PRED40+ (max).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Normalize goals: (1 - MRE) + ACC + PRED
        # Higher is better.
        return (1.0 - r[mre_idx]) + r[acc_idx] + r[pred_idx]

    # If this is the first row, we can't know if it's the best yet.
    if not seen:
        return False

    current_score = get_score(row)
    seen_scores = [get_score(r) for r in seen]
    
    # We stop if the current row is better than 95% of what we have seen so far.
    # This acts as an early stopping criterion for an online optimization.
    threshold = sorted(seen_scores)[int(len(seen_scores) * 0.95)]
    
    return current_score >= threshold

def run_simulation():
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
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopped at row {i+1}: Found a setup good enough to ship.")
            print(f"Row data: {row}")
            return
        seen.append(row)
    print("Reached end of data without finding a 'good enough' setup.")

if __name__ == "__main__":
    run_simulation()
