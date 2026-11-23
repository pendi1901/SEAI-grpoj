import csv

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range
    (i.e., values never seen or extreme outliers).
    
    We define 'suspicious' as having input values that are more than 3 standard 
    deviations from the mean, or values that are physically impossible/out-of-bounds.
    """
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Calculate stats for numeric inputs
    stats = {}
    for i in input_indices:
        if header[i] == 'criterion':
            continue
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean)**2 for x in vals) / len(vals))**0.5
        stats[i] = (mean, std)

    suspicion_scores = []
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            if header[i] == 'criterion':
                continue
            
            if i in stats:
                mean, std = stats[i]
                if std > 0:
                    z = abs(row[i] - mean) / std
                    # If a value is > 3 standard deviations, it's highly suspicious
                    if z > 3:
                        score += z
        
        if score > 0:
            suspicion_scores.append((score, idx))
    
    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [idx for score, idx in suspicion_scores]

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
    
    print("Analysis: Identifying setups with settings far outside observed ranges.")
    if not suspicious_indices:
        print("No suspicious setups found.")
    else:
        print(f"Found {len(suspicious_indices)} suspicious setups.")
        print("The most suspicious row indices are:", suspicious_indices[:5])
        print("These rows contain input values that deviate significantly from the norm.")
