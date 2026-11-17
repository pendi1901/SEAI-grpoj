import csv

def spot(header, rows):
    """
    Identifies rows that are 'outliers' based on the Mahalanobis-like 
    distance of their input values from the population mean.
    Rows with high input variance are flagged as potentially mistyped.
    """
    # Identify input columns (those not ending in + or -)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Convert rows to numeric inputs
    data = []
    for row in rows:
        data.append([float(row[i]) for i in input_indices])
    
    # Calculate column means and standard deviations
    n = len(data)
    m = len(input_indices)
    means = [sum(data[i][j] for i in range(n)) / n for j in range(m)]
    stdevs = []
    for j in range(m):
        var = sum((data[i][j] - means[j])**2 for i in range(n)) / n
        stdevs.append((var**0.5) if var > 0 else 1.0)
    
    # Calculate anomaly score for each row (sum of squared z-scores)
    scores = []
    for i in range(n):
        z_score_sum = 0
        for j in range(m):
            z = (data[i][j] - means[j]) / stdevs[j]
            z_score_sum += z**2
        scores.append((z_score_sum, i))
    
    # Sort by score descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 1% most suspicious rows
    limit = max(1, int(n * 0.01))
    return [s[1] for s in scores[:limit]]

if __name__ == "__main__":
    filename = "pom3a.train.csv"
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    
    # Clean rows: convert numeric strings to floats
    for row in rows:
        for i in range(len(row)):
            try:
                row[i] = float(row[i])
            except ValueError:
                pass
    
    suspicious_indices = spot(header, rows)
    
    print("Anomaly Detection Report:")
    print(f"Identified {len(suspicious_indices)} rows that appear to be outliers.")
    print("These rows contain input values that deviate significantly from the population norm:")
    for idx in suspicious_indices[:10]: # Print top 10
        print(f"- Row Index: {idx}")
    
    if len(suspicious_indices) > 10:
        print("...")
