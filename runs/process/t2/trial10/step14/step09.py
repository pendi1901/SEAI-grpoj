import csv
import math

def spot(header, rows):
    """
    Identifies rows that contain outliers. We use the Interquartile Range (IQR)
    method on numeric columns to detect values that are statistically 
    unlikely (outside 1.5 * IQR).
    """
    numeric_indices = [i for i, name in enumerate(header) 
                       if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate IQR for each numeric column
    outlier_scores = [0] * len(rows)
    
    for i in numeric_indices:
        vals = sorted([float(row[i]) for row in rows])
        q1 = vals[len(vals) // 4]
        q3 = vals[3 * len(vals) // 4]
        iqr = q3 - q1
        low_bound = q1 - 1.5 * iqr
        high_bound = q3 + 1.5 * iqr
        
        # Increment suspicion score for rows outside bounds
        for r_idx, row in enumerate(rows):
            val = float(row[i])
            if val < low_bound or val > high_bound:
                outlier_scores[r_idx] += 1
                
    # Create list of (index, score) and sort by score descending
    indexed_scores = list(enumerate(outlier_scores))
    indexed_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return indices of rows with at least one outlier, most suspicious first
    return [idx for idx, score in indexed_scores if score > 0]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            suspicious = spot(header, rows)
            
            print("Customer Inquiry: Identifying potentially mistyped or anomalous records.")
            if not suspicious:
                print("No suspicious records found.")
            else:
                print(f"Found {len(suspicious)} suspicious records.")
                print("Top 5 most suspicious row indices:", suspicious[:5])
                print("These rows contain values that deviate significantly from the expected distribution.")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
