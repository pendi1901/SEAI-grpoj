import csv
import math

def spot(header, rows):
    """
    Identifies rows that are 'outliers' based on the Mahalanobis-like distance
    of their input values from the centroid of all input values.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Extract only input columns
    inputs = [[row[i] for i in input_indices] for row in rows]
    
    # Calculate centroid (mean of each input column)
    num_rows = len(inputs)
    num_cols = len(input_indices)
    means = [sum(col) / num_rows for col in zip(*inputs)]
    
    # Calculate standard deviation for each input column
    stdevs = []
    for j in range(num_cols):
        variance = sum((inputs[i][j] - means[j])**2 for i in range(num_rows)) / num_rows
        stdevs.append(math.sqrt(variance) or 1.0) # Avoid division by zero
        
    # Calculate distance for each row (Z-score sum of squares)
    scores = []
    for i, row_inputs in enumerate(inputs):
        dist = 0.0
        for j in range(num_cols):
            z_score = (row_inputs[j] - means[j]) / stdevs[j]
            dist += z_score**2
        scores.append((dist, i))
        
    # Sort by distance descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of the top 5% most suspicious rows
    limit = max(1, num_rows // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float
                processed_row = [float(val) if val.replace('.','',1).isdigit() or '-' in val else val for val in row]
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print(f"Analysis complete. Identified {len(suspicious_indices)} potentially mistyped or outlier rows.")
        print("The most suspicious row indices (in order of concern) are:")
        print(suspicious_indices[:10])
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
