import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' (outliers).
    We define suspicious rows as those that have extreme input values 
    (e.g., values far from the mean/median) or rows that are 
    statistically inconsistent with the rest of the dataset.
    """
    input_indices = [i for i, name in enumerate(header) if name not in ['MRE-', 'ACC+', 'PRED40+']]
    
    # Calculate means and standard deviations for numeric inputs
    stats = {}
    for i in input_indices:
        col_data = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if col_data:
            mean = sum(col_data) / len(col_data)
            std = (sum((x - mean) ** 2 for x in col_data) / len(col_data)) ** 0.5
            stats[i] = (mean, std if std > 0 else 1.0)

    # Score rows based on how many standard deviations they are from the mean
    # Higher score = more suspicious
    suspicion_scores = []
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            if i in stats:
                val = row[i]
                if isinstance(val, (int, float)):
                    mean, std = stats[i]
                    score += abs((val - mean) / std)
                else:
                    # For symbolic, check if it's a rare category
                    col_vals = [r[i] for r in rows]
                    freq = col_vals.count(val) / len(col_vals)
                    if freq < 0.05:  # Rare category
                        score += 2.0
        suspicion_scores.append((score, idx))

    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in suspicion_scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        suspicious_indices = spot(header, rows)
        
        print(f"Identified {len(suspicious_indices)} potentially erroneous rows:")
        for idx in suspicious_indices[:5]:
            print(f"- Row {idx} appears highly anomalous.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
