import csv

def spot(header, rows):
    """
    Identifies rows that are 'unlike anyone we have employed'.
    We use the Mahalanobis-like distance (z-score sum) for numeric inputs.
    A row is suspicious if its input values are extreme outliers compared 
    to the historical distribution of the training data.
    """
    # Identify numeric input columns (exclude goal columns)
    numeric_indices = [
        i for i, h in enumerate(header) 
        if h[0].isupper() and not (h.endswith('+') or h.endswith('-'))
    ]
    
    # Calculate mean and std dev for each numeric input column
    stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        variance = sum((x - mean) ** 2 for x in vals) / len(vals)
        std = variance ** 0.5
        if std > 0:
            stats[i] = (mean, std)
    
    # Score rows based on how many input values are extreme outliers
    # We use a threshold of 3.0 standard deviations
    row_scores = []
    for idx, row in enumerate(rows):
        score = 0.0
        for i in numeric_indices:
            if i in stats and isinstance(row[i], (int, float)):
                mean, std = stats[i]
                z = abs(row[i] - mean) / std
                if z > 3.0:
                    score += z
        
        if score > 0:
            row_scores.append((idx, score))
            
    # Sort by score descending (most suspicious/unlike others first)
    row_scores.sort(key=lambda x: x[1], reverse=True)
    return [item[0] for item in row_scores]

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
    
    print("Analysis: Identifying candidates who are 'unlike anyone we have employed'.")
    print(f"Found {len(suspicious_indices)} rows that deviate significantly from historical norms.")
    print("Top 5 most unique/suspicious rows (estimates for these may be unreliable):")
    for i in suspicious_indices[:5]:
        print(f"- Row {i}: This employee's profile contains extreme values compared to the rest of the staff.")
