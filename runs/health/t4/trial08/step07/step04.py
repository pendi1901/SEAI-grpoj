import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected distribution
    based on the historical 'seen' data.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_utility(r):
        # MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
        # Normalize by using negative MRE
        return -r[mre_idx] + r[acc_idx] + r[pred_idx]

    # If this is the first row, we can't compare yet
    if not seen:
        return False

    current_utility = get_utility(row)
    seen_utilities = [get_utility(r) for r in seen]
    
    # Threshold: Is this row better than 95% of what we have seen so far?
    # We use the 95th percentile of seen data as our stopping criterion.
    seen_utilities.sort()
    threshold_idx = int(len(seen_utilities) * 0.95)
    threshold = seen_utilities[threshold_idx]
    
    return current_utility >= threshold

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopped at row {i+1}: Found a setup good enough to ship.")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("Processed all rows without finding a setup meeting the criteria.")
    
    exit(0)
