import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by detecting outliers in the input space.
    Rows with input values that are statistically far from the mean (z-score > 3)
    are flagged as potentially erroneous entries.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Only consider numeric input columns for outlier detection
    numeric_inputs = []
    for idx in input_indices:
        vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        if vals:
            numeric_inputs.append((idx, vals))

    # Calculate z-scores for each numeric input
    suspicion_scores = [0.0] * len(rows)
    for idx, vals in numeric_inputs:
        mean = sum(vals) / len(vals)
        variance = sum((x - mean) ** 2 for x in vals) / len(vals)
        std = variance ** 0.5
        if std == 0:
            continue
            
        for r_idx, row in enumerate(rows):
            val = row[idx]
            if isinstance(val, (int, float)):
                z_score = abs(val - mean) / std
                # If z-score is high, it's suspicious
                if z_score > 3:
                    suspicion_scores[r_idx] += z_score

    # Sort rows by suspicion score descending
    indexed_scores = sorted(enumerate(suspicion_scores), key=lambda x: x[1], reverse=True)
    
    # Return indices of rows with non-zero suspicion
    return [i for i, score in indexed_scores if score > 0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete. Found {len(suspicious_indices)} potentially erroneous rows.")
    if suspicious_indices:
        print(f"Top 5 most suspicious row indices: {suspicious_indices[:5]}")
        print(f"Data for the most suspicious row: {rows[suspicious_indices[0]]}")
    else:
        print("No suspicious rows detected based on input outliers.")
