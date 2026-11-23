import csv

def remember(header, rows):
    """
    Identifies the best rows by calculating a normalized aggregate score.
    Goals: MRE- (minimize), ACC+ (maximize), PRED40+ (maximize).
    Returns the indices of the top 5% of rows.
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    # Calculate scores for all rows
    scores = []
    for i, row in enumerate(rows):
        # Normalize: (1 - MRE) + ACC + PRED
        # Assuming values are within [0, 1] range
        mre = float(row[idx_mre])
        acc = float(row[idx_acc])
        pred = float(row[idx_pred])
        
        score = (1.0 - mre) + acc + pred
        scores.append((score, i))

    # Sort by score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (max 40 rows for 800 data rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in scores[:limit]]

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
        
        best_indices = remember(header, rows)
        
        print("Top performing configurations identified:")
        print(f"Found {len(best_indices)} setups that maximize performance.")
        print("Indices of the best setups:")
        print(best_indices)
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
