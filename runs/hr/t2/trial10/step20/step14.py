import csv
import step09

def flow(header, row, seen):
    """
    Detects if a team 'no longer looks the way it normally does' by checking
    if the incoming row is an outlier compared to the historical 'seen' data.
    We use the Z-score logic from step09 to identify suspicious shifts.
    """
    if len(seen) < 30:
        return False

    # Identify numeric columns
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    # Calculate stats for the 'seen' population
    stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in seen if isinstance(r[i], (int, float))]
        if len(vals) > 10:
            mean = sum(vals) / len(vals)
            var = sum((x - mean) ** 2 for x in vals) / len(vals)
            std = var ** 0.5
            stats[i] = (mean, std)
            
    # Check if the current row is an outlier (Z > 3)
    score = 0
    for i in numeric_indices:
        if i in stats and isinstance(row[i], (int, float)):
            mean, std = stats[i]
            if std > 0:
                z = abs(row[i] - mean) / std
                if z > 3:
                    score += z
                    
    # If the row is significantly different from the norm, flag it
    return score > 5

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

    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
    
    print("Team Stability Analysis:")
    print(f"Processed {len(rows)} records.")
    print(f"Detected {anomalies} instances where the team composition deviated significantly from historical norms.")
    print("Decision logic: Flagged rows that are statistical outliers (Z-score > 3) compared to previous records.")
