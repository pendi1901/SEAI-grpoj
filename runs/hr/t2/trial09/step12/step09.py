import csv
import step01

def spot(header, rows):
    """
    Identifies rows that look 'wrong' by detecting outliers in numeric columns.
    We calculate the mean and standard deviation for each numeric column and
    flag rows that have values significantly outside the expected range (e.g., 
    more than 3 standard deviations from the mean).
    """
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    # Calculate stats for each numeric column
    stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mean, std)
    
    # Score rows by how many outliers they contain
    # A higher count of extreme outliers makes a row more suspicious
    suspicion_scores = []
    for idx, row in enumerate(rows):
        score = 0
        for i in numeric_indices:
            if i in stats:
                mean, std = stats[i]
                val = row[i]
                if std > 0:
                    z_score = abs(val - mean) / std
                    if z_score > 3:  # Threshold for "wrong" entry
                        score += z_score
        suspicion_scores.append((score, idx))
    
    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of rows with non-zero suspicion scores
    return [item[1] for item in suspicion_scores if item[0] > 0]

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
    
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially erroneous data entries.")
    print(f"Found {len(suspicious_indices)} rows with suspicious numeric values.")
    print("Top 5 most suspicious row indices:")
    for idx in suspicious_indices[:5]:
        print(f"- Row {idx}")
