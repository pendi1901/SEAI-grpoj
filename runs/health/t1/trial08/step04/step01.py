import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We normalize the values and use a simple weighted sum (Pareto-like approach).
    """
    n = len(rows)
    if n == 0:
        return []
    
    # Identify column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Calculate scores
    # Since we want to minimize MRE and maximize ACC/PRED, 
    # we use (1 - MRE) + ACC + PRED as a proxy for "trustworthiness"
    scores = []
    for i, row in enumerate(rows):
        mre = row[mre_idx]
        acc = row[acc_idx]
        pred = row[pred_idx]
        
        # Score calculation: higher is better
        score = (1.0 - mre) + acc + pred
        scores.append((score, i))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (or at least 1)
    limit = max(1, n // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns to floats, keep symbolic as strings
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['criterion']:
                    processed_row.append(val)
                else:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    print(f"Analysis complete. Found {len(best_indices)} unusually trustworthy setups.")
    print("Top row indices:", best_indices)
    print("Example of a top setup:")
    print(rows[best_indices[0]])
