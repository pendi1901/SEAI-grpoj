import csv

def spot(header, rows):
    """
    Identifies rows that contain input values that are suspicious.
    Suspicion is defined by calculating the Z-score of each input feature
    and flagging rows where the sum of squared Z-scores is significantly
    higher than the average, indicating an outlier in the input space.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Extract only input columns
    data = [[row[i] for i in input_indices] for row in rows]
    n = len(data)
    m = len(input_indices)
    
    # Calculate means for each input column
    means = [sum(col) / n for col in zip(*data)]
    
    # Calculate standard deviations
    stdevs = []
    for i in range(m):
        variance = sum((row[i] - means[i])**2 for row in data) / n
        stdevs.append((variance**0.5) + 1e-9)
        
    # Calculate a "suspicion score" for each row
    # We use the sum of squared Z-scores (Mahalanobis distance approximation)
    scores = []
    for idx, row in enumerate(data):
        z_score_sq = 0
        for i in range(m):
            z = (row[i] - means[i]) / stdevs[i]
            z_score_sq += z**2
        scores.append((idx, z_score_sq))
        
    # Sort by score descending (most suspicious first)
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    num_to_return = max(1, n // 20)
    return [s[0] for s in scores[:num_to_return]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to floats
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Anomaly Detection Analysis:")
        print(f"Identified {len(suspicious_indices)} rows that appear to be outliers.")
        print("These rows contain input values that deviate significantly from the")
        print("general distribution of the dataset, suggesting potential data entry errors.")
        print(f"The most suspicious row index is: {suspicious_indices[0]}")
        print(f"Top 5 suspicious indices: {suspicious_indices[:5]}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
