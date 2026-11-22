import csv
import math
from step09 import spot

def flow(header, row, seen):
    """
    Determines if the current row is an outlier compared to the 'seen' population.
    We use the Mahalanobis-like distance logic from step09 to detect if the 
    new row deviates significantly from the distribution of the seen data.
    """
    if not seen:
        return False
    
    # Combine seen rows with the current row to calculate distribution
    all_data = seen + [row]
    
    # Identify numeric columns (excluding goals)
    numeric_indices = [
        i for i, col in enumerate(header) 
        if col[0].isupper() and not (col.endswith('+') or col.endswith('-'))
    ]
    
    # Calculate mean and standard deviation for each column based on 'seen'
    n = len(seen)
    means = [sum(col) / n for col in zip(*[[r[i] for r in seen] for i in numeric_indices])]
    stds = [math.sqrt(sum((r[i] - means[j])**2 for r in seen) / n) 
            for j, i in enumerate(numeric_indices)]
    
    # Calculate z-score for the current row
    score = 0
    for j, i in enumerate(numeric_indices):
        if stds[j] > 0:
            z = (row[i] - means[j]) / stds[j]
            score += z**2
            
    # If the squared z-score sum is significantly high (threshold 3.0), 
    # flag as a team shift/anomaly.
    return score > 3.0

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print(f"Analysis complete: Detected {anomalies} instances where the team composition "
          "deviated significantly from the established historical norm.")
    exit(0)
