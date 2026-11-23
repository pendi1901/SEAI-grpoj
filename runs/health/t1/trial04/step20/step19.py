import csv

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range
    or rare categories, suggesting potential data entry errors.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, name in enumerate(header) if '-' not in name and '+' not in name]
    
    # Calculate statistics for each input column
    stats = {}
    for i in input_indices:
        col_vals = [r[i] for r in rows]
        if isinstance(col_vals[0], (int, float)):
            # Numeric: use mean and standard deviation for outlier detection
            vals = [v for v in col_vals if v is not None]
            mean = sum(vals) / len(vals)
            variance = sum((v - mean) ** 2 for v in vals) / len(vals)
            std = variance ** 0.5
            stats[i] = ('numeric', mean, std if std > 0 else 1.0)
        else:
            # Symbolic: use frequency distribution
            counts = {}
            for v in col_vals:
                counts[v] = counts.get(v, 0) + 1
            stats[i] = ('symbolic', counts, len(rows))

    # Score each row based on how unusual its inputs are
    scores = []
    for idx, row in enumerate(rows):
        suspicion = 0
        for i in input_indices:
            val = row[i]
            if val == "?": continue
            
            stype, s1, s2 = stats[i]
            if stype == 'numeric':
                mean, std = s1, s2
                # Z-score: distance from mean in units of standard deviation
                suspicion += abs(val - mean) / std
            else:
                # Rare category penalty: 1 - frequency
                counts, total = s1, s2
                freq = counts.get(val, 1) / total
                suspicion += (1.0 - freq)
        scores.append((suspicion, idx))
    
    # Sort by suspicion descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in scores]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    print("Analysis complete: Identified rows with potentially erroneous input values.")
    print("The following rows contain settings that are statistically far from the norm:")
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f"- Row {idx} (Suspicion Score: {suspicious_indices[i]:.2f})")
