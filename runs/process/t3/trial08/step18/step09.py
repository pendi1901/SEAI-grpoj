import csv
import math

def spot(header, rows):
    """
    Identifies rows that are outliers using the Isolation Forest concept 
    (or a simplified distance-based anomaly detection).
    Returns the indices of rows that are most suspicious (furthest from the median).
    """
    # Identify numeric input columns (exclude goals)
    input_indices = [i for i, h in enumerate(header) 
                     if h[0].isupper() and not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate median for each input column
    medians = []
    for i in input_indices:
        vals = sorted([row[i] for row in rows if row[i] != "?"])
        medians.append(vals[len(vals) // 2])
    
    # Calculate a "suspicion score" for each row based on Euclidean distance to median
    scores = []
    for idx, row in enumerate(rows):
        dist = 0
        count = 0
        for i, col_idx in enumerate(input_indices):
            val = row[col_idx]
            if val != "?":
                dist += (val - medians[i])**2
                count += 1
        
        # Normalize by number of valid inputs
        score = math.sqrt(dist / count) if count > 0 else 0
        scores.append((score, idx))
    
    # Sort by score descending (most suspicious first)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    return [idx for score, idx in scores if score > 0]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Customer Inquiry: Identifying potentially mistyped or anomalous records.")
        print("-" * 60)
        print(f"Found {len(suspicious_indices)} records that deviate from the norm.")
        print("Top 5 most suspicious row indices:")
        for idx in suspicious_indices[:5]:
            print(f" - Row {idx} (Distance score: {idx})")
            
        print("\nConclusion: These rows contain input values that are statistical outliers.")
        print("We recommend manual verification of these specific entries.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
