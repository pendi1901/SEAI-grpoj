import csv

def flow(header, row, seen):
    """
    Decides whether to accept the current row based on a simple threshold 
    heuristic derived from the distribution of previous rows.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Calculate utility for the current row
    # Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize)
    current_utility = -row[mre_idx] + row[acc_idx] + row[pred_idx]

    if not seen:
        return False

    # Calculate utilities of seen rows
    seen_utilities = []
    for s in seen:
        seen_utilities.append(-s[mre_idx] + s[acc_idx] + s[pred_idx])

    # If current row is better than the 95th percentile of seen rows, accept it
    # This acts as an "early stopping" criterion for a "good enough" setup
    threshold = sorted(seen_utilities)[int(len(seen_utilities) * 0.95)]
    
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
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    seen = []
    found = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Found a setup good enough to ship at row {i+1}.")
            print(f"MRE: {row[0]:.4f}, ACC: {row[1]:.4f}, PRED40: {row[2]:.4f}")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("No setup met the criteria for early shipping.")
