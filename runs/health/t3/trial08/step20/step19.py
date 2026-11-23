import csv

def spot(header, rows):
    """
    Identifies rows that contain input values outside the range of 
    previously seen data (outliers/anomalies).
    
    We define 'suspicious' as any numeric input value that falls 
    outside the [min, max] range observed in the rest of the dataset.
    """
    # Identify numeric input columns (not goals)
    input_indices = [
        i for i, h in enumerate(header) 
        if not (h.endswith('-') or h.endswith('+')) and isinstance(rows[0][i], (int, float))
    ]
    
    # Calculate global min/max for each input column
    col_ranges = {}
    for idx in input_indices:
        values = [row[idx] for row in rows if isinstance(row[idx], (int, float))]
        if values:
            col_ranges[idx] = (min(values), max(values))
    
    suspicion_scores = [0] * len(rows)
    
    # Score rows based on how many inputs are outside the global range
    for i, row in enumerate(rows):
        for idx in input_indices:
            val = row[idx]
            if isinstance(val, (int, float)):
                low, high = col_ranges[idx]
                # If a value is outside the observed range, it is suspicious
                if val < low or val > high:
                    suspicion_scores[i] += 1
    
    # Return indices of rows with suspicion scores > 0, sorted by score descending
    indexed_scores = [(score, i) for i, score in enumerate(suspicion_scores) if score > 0]
    indexed_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [i for score, i in indexed_scores]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
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
        
        if not suspicious_indices:
            print("No suspicious configurations found.")
        else:
            print(f"Analysis complete. Found {len(suspicious_indices)} rows with values outside the observed range.")
            print("Top 10 most suspicious row indices:")
            print(suspicious_indices[:10])
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
