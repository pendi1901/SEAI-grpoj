import csv

def flow(header, row, seen):
    """
    Decides whether to accept the current row based on a threshold derived
    from the distribution of previously seen rows.
    
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # If this is the first row, we can't compare, so keep looking
    if not seen:
        return False

    # Extract goals from seen rows
    mres = [r[mre_idx] for r in seen]
    accs = [r[acc_idx] for r in seen]
    preds = [r[pred_idx] for r in seen]

    # Calculate thresholds (e.g., top 10% performance observed so far)
    # For MRE- (minimize), we want values below the 10th percentile
    # For ACC+ and PRED40+ (maximize), we want values above the 90th percentile
    mre_threshold = sorted(mres)[max(0, len(mres) // 10)]
    acc_threshold = sorted(accs)[max(0, len(accs) - 1 - (len(accs) // 10))]
    pred_threshold = sorted(preds)[max(0, len(preds) - 1 - (len(preds) // 10))]

    # Check if current row meets the "good enough" criteria
    is_good = (row[mre_idx] <= mre_threshold and 
               row[acc_idx] >= acc_threshold and 
               row[pred_idx] >= pred_threshold)

    return is_good

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
        found = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Found a setup good enough to ship at index {i}.")
                found = True
                break
            seen.append(row)
        
        if not found:
            print("No setup met the criteria before the end of the data.")
        
        exit(0)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        exit(1)
