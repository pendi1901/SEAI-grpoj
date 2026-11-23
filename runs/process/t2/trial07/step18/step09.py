import csv
import math

def spot(header, rows):
    """
    Identifies suspicious rows by calculating the Mahalanobis-like distance
    of each row from the centroid of the dataset. Rows with high distance
    are considered outliers (potentially mistyped).
    """
    # Only consider input columns (not goals)
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate mean and standard deviation for each input column
    n = len(rows)
    means = []
    stds = []
    for i in input_indices:
        vals = [row[i] for row in rows]
        mu = sum(vals) / n
        sigma = math.sqrt(sum((x - mu)**2 for x in vals) / n)
        means.append(mu)
        stds.append(sigma if sigma > 0 else 1.0)
    
    # Calculate distance for each row
    distances = []
    for idx, row in enumerate(rows):
        dist = 0
        for j, col_idx in enumerate(input_indices):
            z_score = (row[col_idx] - means[j]) / stds[j]
            dist += z_score**2
        distances.append((math.sqrt(dist), idx))
    
    # Sort by distance descending (most suspicious first)
    distances.sort(key=lambda x: x[0], reverse=True)
    
    return [idx for dist, idx in distances]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])
            
    suspicious_indices = spot(header, rows)
    
    print("Customer Inquiry: Identifying potentially mistyped records.")
    print("Analysis: The following rows are the most statistically anomalous (outliers):")
    for i in range(min(5, len(suspicious_indices))):
        idx = suspicious_indices[i]
        print(f"  - Row {idx} (Distance score: {i+1})")
    print("These records deviate significantly from the patterns observed in the rest of the data.")
