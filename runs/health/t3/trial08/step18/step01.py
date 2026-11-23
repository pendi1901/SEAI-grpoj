import csv

def remember(header, rows):
    """
    Identifies the best rows based on multi-objective optimization.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    We use a simple Pareto-based approach or weighted normalization.
    Given the requirement for 5% of 800 rows (max 40), we return the top 40.
    """
    # Identify indices for goals
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    # Normalize goals to [0, 1] to compare them
    # MRE is minimize (1 - val), others are maximize (val)
    scores = []
    for i, row in enumerate(rows):
        # Simple heuristic: average of normalized objectives
        # Assuming data is within reasonable bounds [0, 1]
        mre = 1.0 - float(row[idx_mre])
        acc = float(row[idx_acc])
        pred = float(row[idx_pred])
        
        # Combined score
        score = (mre + acc + pred) / 3.0
        scores.append((score, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                # Convert numeric columns to float, keep strings as is
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print(f"Analysis complete. Found {len(best_indices)} trustworthy setups.")
        print("Indices of top performing configurations:")
        print(best_indices)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
