import csv
import numpy as np

def flow(header, row, seen):
    """
    Detects if the current row is an outlier compared to the 'seen' distribution.
    We use the Z-score of numeric columns to determine if the current row 
    deviates significantly from the historical average.
    """
    if len(seen) < 30:
        return False

    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    # Extract numeric data from seen rows
    seen_data = np.array([[r[i] for i in numeric_indices] for r in seen])
    current_data = np.array([row[i] for i in numeric_indices])
    
    means = np.mean(seen_data, axis=0)
    stds = np.std(seen_data, axis=0)
    stds[stds == 0] = 1.0  # Avoid division by zero
    
    # Calculate Z-score for the current row
    z_scores = np.abs((current_data - means) / stds)
    avg_z = np.mean(z_scores)
    
    # If the average Z-score is high (e.g., > 3.0), the row is an outlier
    return avg_z > 3.0

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    seen = []
    outliers = 0
    for row in rows:
        if flow(header, row, seen):
            outliers += 1
        seen.append(row)
    
    print("Analysis: Detecting shifts in team composition.")
    print(f"Processed {len(rows)} records.")
    print(f"Number of records flagged as 'not looking normal': {outliers}")
    print("Logic: Flagged rows that deviate significantly (Z-score > 3.0) from the historical mean of numeric attributes.")
