import csv
import numpy as np

def spot(header, rows):
    """
    Identifies suspicious rows (outliers) based on the distribution of input parameters.
    Rows with values significantly outside the expected range (e.g., 3 standard deviations)
    are flagged as potentially entered wrongly.
    """
    suspicious = []
    
    # Identify input columns (those not ending in - or +)
    input_indices = [i for i, h in enumerate(header) if '-' not in h and '+' not in h]
    
    # Calculate Z-scores for numeric inputs to find outliers
    for i in input_indices:
        col_data = [row[i] for row in rows if isinstance(row[i], (int, float))]
        if not col_data:
            continue
            
        mean = np.mean(col_data)
        std = np.std(col_data)
        
        if std == 0:
            continue
            
        for row_idx, row in enumerate(rows):
            val = row[i]
            if isinstance(val, (int, float)):
                z_score = abs((val - mean) / std)
                # If Z-score > 3, it's a statistical outlier
                if z_score > 3:
                    # Store as (row_index, z_score) to sort by suspicion
                    suspicious.append((row_idx, z_score))
    
    # Sort by Z-score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[1], reverse=True)
    
    # Return unique row indices
    seen = set()
    result = []
    for idx, score in suspicious:
        if idx not in seen:
            result.append(idx)
            seen.add(idx)
            
    return result

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
            rows.append(processed_row)

    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete. Found {len(suspicious_indices)} potentially erroneous rows.")
    print("Top 5 most suspicious row indices:", suspicious_indices[:5])
    
    if suspicious_indices:
        print("\nDetails of the most suspicious row:")
        print(rows[suspicious_indices[0]])
