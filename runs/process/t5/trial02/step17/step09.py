import ezr
import random

def spot(header, rows):
    """
    Identify rows that are 'suspicious' by checking if they are outliers
    in the input space. We use the distance to the nearest neighbor in the
    input space (xdist) as a metric. Rows that are very far from all other
    rows are likely to be outliers or 'mistyped'.
    """
    # Create a table to handle normalization and distance calculations
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Calculate the average distance to other rows for each row.
    # A high average distance indicates the row is an outlier.
    # We use a sample to keep this efficient for larger datasets.
    sample_size = min(len(rows), 200)
    sample_rows = random.sample(rows, sample_size)
    
    suspicion_scores = []
    for i, row in enumerate(rows):
        # Calculate distance to all rows in the sample
        distances = [ezr.xdist(tbl, row, other) for other in sample_rows]
        # Use the average of the 5 nearest neighbors as a measure of density
        distances.sort()
        avg_dist = sum(distances[1:6]) / 5
        suspicion_scores.append((avg_dist, i))
    
    # Sort by suspicion score descending (most suspicious first)
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 10 most suspicious rows
    return [item[1] for item in suspicion_scores[:10]]

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify suspicious rows
    random.seed(1234567891)
    suspicious_indices = spot(header, rows)
    
    print("--- Outlier Detection Analysis ---")
    print("The following rows are the most suspicious (potential data entry errors):")
    for idx in suspicious_indices:
        print(f"Row {idx}: {rows[idx]}")
    
    print("\nThese rows were identified as outliers based on their distance from")
    print("the rest of the input data distribution.")
