import csv

def spot(header, rows):
    """
    Identifies rows that look wrong by checking for outliers in numeric columns.
    A row is suspicious if it contains a value that is significantly outside
    the range (e.g., 4 standard deviations) of its column.
    """
    numeric_indices = [i for i, h in enumerate(header) if h[0].isupper()]
    
    # Calculate stats for each numeric column
    stats = {}
    for i in numeric_indices:
        vals = [row[i] for row in rows if isinstance(row[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mean, std)

    # Score rows based on how many standard deviations they are from the mean
    scores = []
    for row_idx, row in enumerate(rows):
        row_score = 0
        for i in numeric_indices:
            if i in stats and isinstance(row[i], (int, float)):
                mean, std = stats[i]
                if std > 0:
                    z_score = abs(row[i] - mean) / std
                    if z_score > 4:  # Threshold for "wrong" entry
                        row_score += z_score
        if row_score > 0:
            scores.append((row_score, row_idx))
    
    # Sort by most suspicious (highest score)
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.train.csv"
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
    
    print("Analysis complete. Rows with potentially erroneous data (most suspicious first):")
    for idx in suspicious_indices[:10]:
        print(f"- Row index {idx} contains values that are statistical outliers.")
