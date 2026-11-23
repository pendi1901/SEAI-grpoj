import csv
import step09

def flow(header, row, seen):
    """
    Detects if a new row is an outlier compared to the 'seen' data.
    We use the logic from step09 (Z-score > 3) to determine if the 
    team composition has shifted significantly.
    """
    if not seen:
        return False
    
    # Combine seen rows with the current row to calculate current distribution
    all_rows = seen + [row]
    
    # Identify numeric columns
    numeric_indices = [i for i, name in enumerate(header) if name[0].isupper()]
    
    # Check if the current row (the last one) is an outlier
    for idx in numeric_indices:
        col_vals = [r[idx] for r in all_rows if isinstance(r[idx], (int, float))]
        if len(col_vals) < 10: # Need enough data to establish a norm
            continue
            
        mean = sum(col_vals) / len(col_vals)
        variance = sum((x - mean) ** 2 for x in col_vals) / len(col_vals)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            continue
            
        val = row[idx]
        if isinstance(val, (int, float)):
            z_score = abs(val - mean) / std_dev
            # If the new row is more than 3 standard deviations away, 
            # the team no longer looks the way it normally does.
            if z_score > 3:
                return True
                
    return False

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
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print("Team Composition Analysis:")
    print(f"Processed {len(rows)} records.")
    print(f"Detected {anomalies} instances where the team composition shifted significantly.")
    print("Logic: A shift is flagged when a new record is an extreme outlier (Z-score > 3) in numeric metrics.")
