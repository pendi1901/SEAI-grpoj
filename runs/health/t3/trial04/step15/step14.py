import csv

def get_score(header, row):
    """
    Calculates aggregate score: (1 - MRE) + ACC + PRED40.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Normalize MRE (minimize) by subtracting from 1.0
    return (1.0 - float(row[mre_idx])) + float(row[acc_idx]) + float(row[pred_idx])

def flow(header, row, seen):
    """
    Decides if the current row is the best we are likely to see.
    We stop when the current row's score is significantly better than 
    the previous best, or if we have processed a sufficient number of 
    rows without improvement (early stopping).
    """
    if not seen:
        return False
    
    current_score = get_score(header, row)
    best_seen_score = max(get_score(header, r) for r in seen)
    
    # If the current row is the best we've seen so far, we consider it
    # a candidate for stopping. To avoid stopping too early, we only
    # stop if we have seen a reasonable number of samples (e.g., 50).
    if current_score > best_seen_score and len(seen) > 50:
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
                # criterion is at index 4
                if i == 4:
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    seen = []
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopping criteria met at row {i + 1}.")
            print(f"The best configuration found has an aggregate score of {get_score(header, row):.4f}.")
            stopped = True
            break
        seen.append(row)
        
    if not stopped:
        print("Processed all rows without finding a definitive stopping point.")
