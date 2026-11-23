import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the potential distribution
    based on the data seen so far.
    """
    if not seen:
        return False

    # Identify goal indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # We use the same normalization logic as step01, but relative to 'seen'
        # To avoid re-normalizing everything, we use a simple heuristic:
        # A row is 'good' if it outperforms the average of the 'seen' rows.
        # MRE- (lower is better), ACC+ (higher is better), PRED40+ (higher is better)
        mre_avg = sum(s[mre_idx] for s in seen) / len(seen)
        acc_avg = sum(s[acc_idx] for s in seen) / len(seen)
        pred_avg = sum(s[pred_idx] for s in seen) / len(seen)
        
        return (row[mre_idx] < mre_avg) and (row[acc_idx] > acc_avg) and (row[pred_idx] > pred_avg)

    # Stop if we have seen enough data and this row is significantly better
    # than the average of what we have seen so far.
    if len(seen) > 50 and get_score(row):
        return True
    return False

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        seen = []
        found = False
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                print(f"Stopped at row {i}: Found a setup good enough to ship.")
                print(f"MRE={row[0]:.4f}, ACC={row[1]:.4f}, PRED40={row[2]:.4f}")
                found = True
                break
            seen.append(row)
        
        if not found:
            print("Finished all rows without finding a setup good enough to ship.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
