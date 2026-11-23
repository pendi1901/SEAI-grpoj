import csv

def spot(header, rows):
    """
    Identifies rows that look 'wrong' by checking for outliers in numeric columns.
    A row is suspicious if its values deviate significantly from the column mean
    (using Z-score logic).
    """
    suspicious = []
    
    # Identify numeric columns
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    # Calculate means and standard deviations for each numeric column
    stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        var = sum((x - mean) ** 2 for x in vals) / len(vals)
        std = var ** 0.5
        stats[i] = (mean, std)
        
    # Score rows based on how many standard deviations they are from the mean
    row_scores = []
    for idx, row in enumerate(rows):
        score = 0
        for i in numeric_indices:
            if i in stats and isinstance(row[i], (int, float)):
                mean, std = stats[i]
                if std > 0:
                    # Z-score: how many std devs away from mean
                    z = abs(row[i] - mean) / std
                    if z > 3:  # Threshold for outlier
                        score += z
        if score > 0:
            row_scores.append((idx, score))
            
    # Sort by score descending
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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspects = spot(header, rows)
    
    print("Top 5 most suspicious rows (potential data entry errors):")
    for idx in suspects[:5]:
        print(f"Row {idx} is highly suspicious.")
