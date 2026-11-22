import csv

def flow(header, row, seen):
    """
    Decides if the current row is 'good enough' to stop searching.
    We define 'good enough' as being in the top 5% of the expected 
    distribution based on the historical data (the 'seen' rows).
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def calculate_score(r):
        # MRE is minimize, ACC/PRED are maximize.
        # Normalize by assuming values are in [0, 1] range.
        return (1.0 - r[mre_idx]) + r[acc_idx] + r[pred_idx]

    # If this is the first row, we have no baseline to compare against.
    if not seen:
        return False

    # Calculate score for current row
    current_score = calculate_score(row)

    # Calculate scores for all seen rows
    seen_scores = [calculate_score(r) for r in seen]
    
    # We define 'good enough' as being better than 95% of what we have seen so far.
    # This acts as an adaptive threshold.
    threshold = sorted(seen_scores, reverse=True)[max(0, int(len(seen_scores) * 0.05))]
    
    return current_score >= threshold

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                # Numeric columns are those that are uppercase or specific known ones
                if header[i].isupper() or header[i] in ['N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
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
    else:
        print("Processed all rows without finding a setup meeting the criteria.")
