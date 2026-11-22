import csv

def spot(header, rows):
    """
    Identifies rows that are outliers in the input space.
    Uses a simple Z-score approach on numeric input columns to detect
    rows that contain values significantly far from the mean.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Extract numeric input data
    numeric_inputs = []
    for row in rows:
        numeric_inputs.append([row[i] for i in input_indices])
    
    # Calculate means and standard deviations for each input column
    num_cols = len(input_indices)
    num_rows = len(rows)
    
    means = []
    stds = []
    for j in range(num_cols):
        col_vals = [numeric_inputs[i][j] for i in range(num_rows)]
        mean = sum(col_vals) / num_rows
        variance = sum((x - mean) ** 2 for x in col_vals) / num_rows
        std = variance ** 0.5
        means.append(mean)
        stds.append(std if std > 0 else 1.0)
    
    # Calculate an anomaly score for each row (sum of absolute Z-scores)
    scores = []
    for i in range(num_rows):
        z_score_sum = 0
        for j in range(num_cols):
            z_score_sum += abs((numeric_inputs[i][j] - means[j]) / stds[j])
        scores.append((z_score_sum, i))
    
    # Sort by anomaly score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    k = max(1, int(num_rows * 0.05))
    return [item[1] for item in scores[:k]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Anomaly Detection Report")
        print("-" * 30)
        print(f"Identified {len(suspicious_indices)} rows as potentially mistyped or outliers.")
        print("Most suspicious row indices:")
        print(suspicious_indices[:10])
        print("\nThese rows exhibit input values that deviate significantly from the dataset norms.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
