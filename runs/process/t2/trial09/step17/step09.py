import csv
import math

def spot(header, rows):
    """
    Identifies rows that are outliers. We calculate the Mahalanobis-like 
    distance for each row based on input columns. Rows with high 
    deviations from the mean are considered suspicious.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate means and standard deviations for input columns
    means = []
    stds = []
    for i in input_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        mu = sum(vals) / len(vals)
        sigma = math.sqrt(sum((x - mu)**2 for x in vals) / len(vals))
        means.append(mu)
        stds.append(sigma if sigma > 0 else 1.0)
    
    # Calculate a "suspicion score" for each row based on Z-score distance
    scores = []
    for row_idx, row in enumerate(rows):
        dist = 0
        for j, col_idx in enumerate(input_indices):
            val = row[col_idx]
            if isinstance(val, (int, float)):
                z = (val - means[j]) / stds[j]
                dist += z**2
        scores.append((dist, row_idx))
    
    # Sort by distance descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return the indices of the top 5% most suspicious rows
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
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
            
            suspicious = spot(header, rows)
            
            print("Customer Inquiry: Which records look mistyped or made up?")
            print(f"Analysis: Found {len(suspicious)} suspicious records.")
            print(f"Top 5 most suspicious row indices: {suspicious[:5]}")
            print("These rows deviate significantly from the input patterns of the rest of the data.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
