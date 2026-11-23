import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by detecting outliers in the input space.
    Rows with input values that are extreme (e.g., far from the mean/median) 
    relative to the rest of the dataset are flagged as potential errors.
    """
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate statistics for each input column to find outliers
    # We use Z-score approach: (val - mean) / std_dev
    suspicion_scores = [0.0] * len(rows)
    
    for idx in input_indices:
        col_vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        if not col_vals:
            continue
            
        mean = sum(col_vals) / len(col_vals)
        variance = sum((x - mean) ** 2 for x in col_vals) / len(col_vals)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            continue
            
        for i, row in enumerate(rows):
            val = row[idx]
            if isinstance(val, (int, float)):
                z_score = abs(val - mean) / std_dev
                # If Z-score is very high, it's an outlier
                if z_score > 3:
                    suspicion_scores[i] += z_score
                    
    # Create list of (index, score)
    indexed_scores = list(enumerate(suspicion_scores))
    # Filter out rows with 0 suspicion
    suspicious = [item for item in indexed_scores if item[1] > 0]
    # Sort by score descending
    suspicious.sort(key=lambda x: x[1], reverse=True)
    
    return [item[0] for item in suspicious]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete. Found {len(suspicious_indices)} suspicious rows.")
    if suspicious_indices:
        print("Top 5 most suspicious row indices (0-indexed):")
        for idx in suspicious_indices[:5]:
            print(f"Row {idx}: {rows[idx]}")
