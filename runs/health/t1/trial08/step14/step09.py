import csv

def spot(header, rows):
    """
    Identifies rows that look like failed runs.
    A failed run is characterized by extreme outliers in input parameters
    or goals that are physically impossible/highly improbable given the 
    distribution of the rest of the data.
    """
    # Identify numeric columns
    numeric_indices = [i for i, name in enumerate(header) if name not in ['criterion']]
    
    # Calculate Z-scores for numeric columns to find outliers
    # A row is suspicious if it has multiple extreme values (Z > 3)
    suspicion_scores = []
    
    # Pre-calculate means and std devs for numeric columns
    stats = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals: continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean)**2 for x in vals) / len(vals))**0.5
        stats[i] = (mean, std)

    for idx, row in enumerate(rows):
        score = 0
        for i in numeric_indices:
            if i in stats:
                mean, std = stats[i]
                if std > 0:
                    z = abs(row[i] - mean) / std
                    if z > 3:
                        score += z
        suspicion_scores.append((score, idx))
    
    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of rows with non-zero suspicion
    return [idx for score, idx in suspicion_scores if score > 0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete. Identified {len(suspicious_indices)} potentially failed runs.")
    print("Top 5 most suspicious row indices:", suspicious_indices[:5])
    if suspicious_indices:
        print("Example of a suspicious row (index {}):".format(suspicious_indices[0]))
        print(rows[suspicious_indices[0]])
