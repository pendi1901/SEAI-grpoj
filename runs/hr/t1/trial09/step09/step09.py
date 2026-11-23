import csv

def spot(header, rows):
    """
    Identifies suspicious rows by looking for outliers in numeric columns.
    A row is suspicious if it contains values that are significantly 
    outside the range (mean +/- 3 standard deviations) of the column.
    """
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    # Calculate stats for each numeric column
    stats = {}
    for i in numeric_indices:
        vals = [row[i] for row in rows if isinstance(row[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mean, std)
    
    # Score rows based on how many outliers they contain
    suspicion_scores = []
    for idx, row in enumerate(rows):
        score = 0
        for i in numeric_indices:
            if i in stats:
                mean, std = stats[i]
                val = row[i]
                # If std is 0, skip to avoid division by zero
                if std > 0:
                    z_score = abs(val - mean) / std
                    # If value is > 3 standard deviations, it's highly suspicious
                    if z_score > 3:
                        score += z_score
        suspicion_scores.append((score, idx))
    
    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of rows with non-zero suspicion scores
    return [idx for score, idx in suspicion_scores if score > 0]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    print("Data Integrity Analysis: Suspicious Rows")
    print("----------------------------------------")
    if not suspicious_indices:
        print("No suspicious data entries found.")
    else:
        print(f"Found {len(suspicious_indices)} rows with potential data entry errors.")
        print("Top 10 most suspicious row indices:")
        for idx in suspicious_indices[:10]:
            print(f"- Row index: {idx}")
    
    exit(0)
