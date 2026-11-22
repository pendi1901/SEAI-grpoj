import csv

def spot(header, rows):
    """
    Identifies rows that look wrong by checking for outliers in numeric columns.
    We calculate the Z-score for each numeric input and flag rows where any 
    value is more than 3 standard deviations from the mean.
    """
    numeric_indices = [i for i, h in enumerate(header) if h[0].isupper()]
    
    # Calculate means and std devs for numeric columns
    stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mean, std)
    
    # Score rows based on how many standard deviations they are from the mean
    # A higher score indicates more "suspicious" values
    suspicious = []
    for idx, row in enumerate(rows):
        row_score = 0
        for i in numeric_indices:
            if i in stats:
                mean, std = stats[i]
                if std > 0:
                    z = abs(row[i] - mean) / std
                    if z > 3:
                        row_score += z
        if row_score > 0:
            suspicious.append((row_score, idx))
            
    # Sort by score descending
    suspicious.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in suspicious]

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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    suspects = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print(f"Found {len(suspects)} rows with suspicious numeric values (outliers).")
    print("Top 5 most suspicious row indices:")
    for idx in suspects[:5]:
        print(f"- Row {idx}")
    print("\nLogic: Rows are flagged if they contain values > 3 standard deviations from the column mean.")
