import csv

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range 
    (outliers) for each numeric input column. Returns the indices of these 
    rows, sorted by the total 'suspicion' score (sum of Z-scores).
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Store suspicion scores for each row
    suspicion_scores = [0.0] * len(rows)
    
    for idx in input_indices:
        # Extract numeric values for this column
        col_vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        if not col_vals:
            continue
            
        # Calculate mean and standard deviation
        n = len(col_vals)
        mean = sum(col_vals) / n
        variance = sum((x - mean) ** 2 for x in col_vals) / n
        std_dev = variance ** 0.5
        
        # If std_dev is 0, all values are the same; no outliers possible
        if std_dev == 0:
            continue
            
        # Flag values that are more than 3 standard deviations from the mean
        for i, row in enumerate(rows):
            val = row[idx]
            if isinstance(val, (int, float)):
                z_score = abs(val - mean) / std_dev
                if z_score > 3:
                    suspicion_scores[i] += z_score
                    
    # Create list of (index, score) for rows with non-zero suspicion
    indexed_scores = [(i, s) for i, s in enumerate(suspicion_scores) if s > 0]
    
    # Sort by score descending (most suspicious first)
    indexed_scores.sort(key=lambda x: x[1], reverse=True)
    
    return [item[0] for item in indexed_scores]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for line in reader:
                processed_row = []
                for i, val in enumerate(line):
                    # criterion is the only symbolic column
                    if header[i] == 'criterion':
                        processed_row.append(val)
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print(f"Analysis complete. Found {len(suspicious_indices)} rows with values far outside observed ranges.")
        if suspicious_indices:
            print("Top 5 most suspicious row indices (0-indexed):")
            for idx in suspicious_indices[:5]:
                print(f"Row {idx}: {rows[idx]}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
