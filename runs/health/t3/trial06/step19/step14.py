import csv

def get_utility(header, row):
    """
    Calculates a normalized utility score for a row.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Normalize goals to [0, 1]
    # MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
    # We use a simple heuristic for normalization based on the problem domain
    mre = min(1.0, max(0.0, row[mre_idx]))
    acc = min(1.0, max(0.0, row[acc_idx]))
    pred = min(1.0, max(0.0, row[pred_idx]))
    
    return (1.0 - mre) + acc + pred

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We stop if the current row's utility is significantly better than 
    the best seen so far, or if we have seen enough rows that 
    further improvement is unlikely.
    """
    if not seen:
        return False
    
    current_utility = get_utility(header, row)
    seen_utilities = [get_utility(header, r) for r in seen]
    best_seen = max(seen_utilities)
    
    # If we have seen at least 100 rows and the current row is not 
    # significantly better than the best seen, we stop.
    # "Significantly better" here is defined as a 5% improvement.
    if len(seen) >= 100:
        if current_utility <= best_seen * 1.05:
            return True
            
    return False

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    seen = []
    stopped_at = -1
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            stopped_at = i + 1
            break
        seen.append(row)

    if stopped_at != -1:
        print(f"Optimization stopped at run {stopped_at}.")
        print("The performance has plateaued; further runs are unlikely to yield significant improvements.")
    else:
        print("The search completed all runs without a significant plateau.")
