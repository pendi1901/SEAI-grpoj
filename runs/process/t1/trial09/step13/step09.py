import csv

def spot(header, rows):
    """
    Identifies suspicious rows by calculating the Mahalanobis-like distance
    (z-score deviation) for each numeric input column. Rows with values 
    significantly outside the expected range (e.g., > 3 standard deviations) 
    are flagged as suspicious.
    """
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    # Calculate mean and standard deviation for each input column
    stats = {}
    for i in input_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        std = (sum((x - mean) ** 2 for x in vals) / len(vals)) ** 0.5
        stats[i] = (mean, std)

    # Score each row based on the maximum z-score of its inputs
    scores = []
    for row_idx, row in enumerate(rows):
        max_z = 0
        for i in input_indices:
            if i in stats:
                mean, std = stats[i]
                if std > 0:
                    z = abs(row[i] - mean) / std
                    if z > max_z:
                        max_z = z
        scores.append((max_z, row_idx))

    # Sort by suspicion score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of rows with high deviation (e.g., z > 3)
    return [idx for score, idx in scores if score > 3.0]

def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            processed = []
            for val in row:
                try:
                    processed.append(float(val))
                except ValueError:
                    processed.append(val)
            rows.append(processed)
    return header, rows

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        header, rows = load_data(filename)
        suspicious_indices = spot(header, rows)
        
        print(f"Analysis complete. Identified {len(suspicious_indices)} potentially mistyped records.")
        if suspicious_indices:
            print("The most suspicious row indices are:")
            print(suspicious_indices[:10])
            print("These rows contain input values that deviate significantly from the population norm.")
        else:
            print("No significantly anomalous records were detected.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
