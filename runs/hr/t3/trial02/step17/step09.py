import csv

def spot(header, rows):
    """
    Identifies suspicious rows by checking for outliers in numeric columns.
    A row is considered suspicious if it contains values that are statistically
    improbable (e.g., outside 3 standard deviations from the mean).
    """
    suspicious_scores = {}

    # Identify numeric columns
    numeric_indices = [i for i, col in enumerate(header) if col[0].isupper()]

    # Calculate mean and std for each numeric column
    stats = {}
    for i in numeric_indices:
        vals = [row[i] for row in rows if isinstance(row[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mean, std)

    # Score rows based on how many standard deviations values are from the mean
    for row_idx, row in enumerate(rows):
        score = 0
        for i in numeric_indices:
            if i in stats:
                mean, std = stats[i]
                if std > 0:
                    val = row[i]
                    z_score = abs(val - mean) / std
                    # If a value is more than 4 standard deviations away, it's highly suspicious
                    if z_score > 4:
                        score += z_score
        
        if score > 0:
            suspicious_scores[row_idx] = score

    # Return indices sorted by suspicion score descending
    return sorted(suspicious_scores, key=suspicious_scores.get, reverse=True)

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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspects = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print(f"Found {len(suspects)} rows with suspicious numeric values.")
    print("Top 5 most suspicious row indices:")
    for idx in suspects[:5]:
        print(f" - Row {idx}")
    
    print("\nStrategy: Rows were flagged if they contained numeric values significantly "
          "outside the expected distribution (Z-score > 4).")
