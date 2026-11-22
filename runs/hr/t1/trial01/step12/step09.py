import csv

def spot(header, rows):
    """
    Identifies suspicious rows by checking for outliers in numeric columns.
    A row is considered suspicious if it contains values that are statistically
    improbable (e.g., outside 3 standard deviations from the mean).
    """
    suspicious = []
    num_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    # Calculate stats for each numeric column
    stats = {}
    for i in num_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals:
            continue
        mu = sum(vals) / len(vals)
        sigma = (sum((x - mu) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mu, sigma)
    
    # Score rows based on how many values are extreme outliers
    row_scores = []
    for idx, row in enumerate(rows):
        score = 0
        for i in num_indices:
            if i in stats:
                mu, sigma = stats[i]
                if sigma > 0:
                    val = row[i]
                    # Z-score check: values > 3 standard deviations are highly suspicious
                    z = abs(val - mu) / sigma
                    if z > 3:
                        score += z
        if score > 0:
            row_scores.append((score, idx))
            
    # Sort by score descending
    row_scores.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in row_scores]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    print("Suspicious rows identified (potential data entry errors):")
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f"- Row {idx} (Score: {i+1})")
    
    if not suspicious_indices:
        print("No suspicious rows found.")
    else:
        print("\nThese rows contain values that deviate significantly from the dataset norms.")
