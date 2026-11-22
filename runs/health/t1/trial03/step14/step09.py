import csv

def spot(header, rows):
    """
    Identifies rows that look like 'failed runs'.
    A failed run is defined here as a row where the input parameters are 
    at extreme, potentially invalid boundaries, or where the goal values 
    are inconsistent with the input settings (outliers).
    """
    # Identify indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # We look for rows that are statistical outliers in the goal space
    # relative to their input settings.
    # A simple approach: calculate the Z-score of the goals.
    # Rows with very high MRE and very low ACC/PRED are suspicious.
    
    def get_score(row):
        # Normalize goals: MRE- (min), ACC+ (max), PRED40+ (max)
        # We use a simple aggregate: (MRE_norm + (1-ACC_norm) + (1-PRED_norm))
        # Higher score = more suspicious
        return row[mre_idx] - row[acc_idx] - row[pred_idx]

    scores = []
    for i, row in enumerate(rows):
        scores.append((get_score(row), i))
    
    # Sort by score descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    header = []
    
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
            
    suspicious = spot(header, rows)
    
    print(f"Identified {len(suspicious)} potentially failed/erroneous runs.")
    print("Top 5 most suspicious row indices:")
    for idx in suspicious[:5]:
        print(f"Row {idx}: {rows[idx]}")
