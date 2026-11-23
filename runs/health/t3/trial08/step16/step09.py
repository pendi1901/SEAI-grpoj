import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' (outliers).
    We use the Interquartile Range (IQR) method on numeric input columns
    to find rows with values that deviate significantly from the norm.
    """
    # Identify numeric input columns (not goals)
    input_indices = [
        i for i, h in enumerate(header) 
        if not (h.endswith('-') or h.endswith('+')) and isinstance(rows[0][i], (int, float))
    ]
    
    suspicion_scores = [0] * len(rows)
    
    for idx in input_indices:
        values = [row[idx] for row in rows]
        q1 = sorted(values)[len(values) // 4]
        q3 = sorted(values)[3 * len(values) // 4]
        iqr = q3 - q1
        
        # Define bounds for outliers
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # If IQR is 0, skip this column to avoid false positives
        if iqr == 0:
            continue
            
        for i, val in enumerate(values):
            if val < lower_bound or val > upper_bound:
                suspicion_scores[i] += 1
                
    # Get indices of rows with suspicion scores > 0, sorted by score descending
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
        
        print(f"Analysis complete. Found {len(suspicious_indices)} suspicious rows.")
        print("Top 10 most suspicious row indices:")
        print(suspicious_indices[:10])
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
