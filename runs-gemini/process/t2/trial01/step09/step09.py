import csv

def spot(header, rows):
    """
    Identifies rows that are 'outliers' in the input space.
    We use the Z-score (standard deviation) approach on input columns.
    Rows with values significantly far from the mean are flagged as suspicious.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate means and standard deviations for each input column
    stats = []
    for i in input_indices:
        vals = [float(row[i]) for row in rows]
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats.append((i, mean, std))
    
    # Score each row by the maximum Z-score of its inputs
    suspicion_scores = []
    for idx, row in enumerate(rows):
        max_z = 0
        for i, mean, std in stats:
            if std > 0:
                z = abs(float(row[i]) - mean) / std
                if z > max_z:
                    max_z = z
        suspicion_scores.append((max_z, idx))
    
    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 1% most suspicious rows
    limit = max(1, len(rows) // 100)
    return [item[1] for item in suspicion_scores[:limit]]

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    rows = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)
            
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying potentially mistyped or anomalous records.")
    print(f"Found {len(suspicious_indices)} suspicious rows based on input distribution.")
    print("Top 5 most suspicious row indices:")
    for idx in suspicious_indices[:5]:
        print(f"- Row {idx}")
