import csv

def spot(header, rows):
    """
    Identifies suspicious rows by looking for outliers in numeric input columns.
    A row is considered suspicious if its values are statistically improbable 
    (e.g., more than 3 standard deviations from the mean) compared to the 
    rest of the population.
    """
    input_indices = [
        i for i, name in enumerate(header) 
        if name[0].isupper() and not (name.endswith('+') or name.endswith('-'))
    ]
    
    # Calculate mean and std dev for each numeric input column
    stats = {}
    for i in input_indices:
        col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not col_vals:
            continue
        mean = sum(col_vals) / len(col_vals)
        var = sum((x - mean) ** 2 for x in col_vals) / len(col_vals)
        std = var ** 0.5
        stats[i] = (mean, std)

    # Score rows based on how many standard deviations they are from the mean
    # across all input columns.
    suspicion_scores = []
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            if i in stats and isinstance(row[i], (int, float)):
                mean, std = stats[i]
                if std > 0:
                    # Z-score calculation
                    z = abs(row[i] - mean) / std
                    if z > 3:  # Threshold for outlier
                        score += z
        if score > 0:
            suspicion_scores.append((score, idx))
    
    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion_scores]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspicious_indices = spot(header, rows)
    
    print("Data Integrity Report: Suspicious Records")
    print("The following rows contain input values that are statistical outliers:")
    for idx in suspicious_indices[:10]:
        print(f"- Row index {idx} appears suspicious.")
    
    if not suspicious_indices:
        print("No suspicious records found.")
    else:
        print(f"\nTotal of {len(suspicious_indices)} records flagged for manual review.")
