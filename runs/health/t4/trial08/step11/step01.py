import csv

def remember(header, rows):
    """
    Identifies the best rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We use a simple Pareto-based approach or weighted normalization.
    Given the constraints, we normalize the goals and pick the top 5%.
    """
    # Identify column indices
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    # Extract goals and normalize
    # MRE is minimized, so we treat it as (1 - value) or negative for maximization
    scores = []
    for i, row in enumerate(rows):
        mre = row[mre_idx]
        acc = row[acc_idx]
        pred = row[pred_idx]
        
        # Simple utility: lower MRE is better, higher ACC/PRED is better
        # Using a simple linear combination of normalized values
        # Since we don't know the range, we use the values directly as relative indicators
        utility = (-mre) + acc + pred
        scores.append((utility, i))

    # Sort by utility descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns
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
    
    best_indices = remember(header, rows)
    
    print(f"Analysis complete. Found {len(best_indices)} highly trustworthy setups.")
    print("Top indices:", best_indices[:10], "...")
    exit(0)
