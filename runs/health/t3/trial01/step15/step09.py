import csv

def spot(header, rows):
    """
    Identifies rows that look like failed runs. 
    A 'failed' run is defined as an outlier in the input space.
    We use the Interquartile Range (IQR) method on numeric inputs to 
    detect values that are statistically anomalous.
    """
    numeric_indices = [
        i for i, name in enumerate(header) 
        if name not in ['criterion', 'MRE-', 'ACC+', 'PRED40+']
    ]
    
    # Calculate IQR for each numeric input column
    outlier_scores = [0] * len(rows)
    
    for i in numeric_indices:
        col_values = [row[i] for row in rows]
        sorted_vals = sorted(col_values)
        q1 = sorted_vals[int(0.25 * len(sorted_vals))]
        q3 = sorted_vals[int(0.75 * len(sorted_vals))]
        iqr = q3 - q1
        
        # Define bounds for outliers
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Increment score for rows outside bounds
        for r_idx, row in enumerate(rows):
            if row[i] < lower_bound or row[i] > upper_bound:
                outlier_scores[r_idx] += 1
                
    # Create list of (index, score) and sort by score descending
    indexed_scores = list(enumerate(outlier_scores))
    indexed_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return indices of rows with at least one outlier, most suspicious first
    return [idx for idx, score in indexed_scores if score > 0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    print(f"Detected {len(suspicious_indices)} potentially failed runs.")
    print("Top 10 most suspicious row indices:")
    print(suspicious_indices[:10])
