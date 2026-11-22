import csv

def flow(header, row, seen):
    """
    Detects if a team's composition has shifted significantly.
    We monitor the mean of 'YearsAtCompany+' and 'JobSatisfaction'.
    If the current row's metrics deviate by more than 2 standard deviations
    from the historical mean of the 'seen' rows, we flag it as an anomaly.
    """
    if not seen:
        return False

    # Identify goal and key metrics
    yac_idx = header.index('YearsAtCompany+')
    js_idx = header.index('JobSatisfaction')
    
    # Only consider numeric metrics for drift detection
    metrics = [yac_idx, js_idx]
    
    # Calculate stats for seen data
    for m_idx in metrics:
        vals = [r[m_idx] for r in seen]
        mean = sum(vals) / len(vals)
        var = sum((x - mean) ** 2 for x in vals) / len(vals)
        std = var ** 0.5
        
        # If std is 0, we can't detect drift on this metric
        if std == 0:
            continue
            
        # Check if current row is an outlier (> 2 std devs)
        if abs(row[m_idx] - mean) > (2 * std):
            return True
            
    return False

def load_data(filename):
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
    return header, rows

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    header, rows = load_data(filename)
    
    seen = []
    anomalies = 0
    for row in rows:
        if flow(header, row, seen):
            anomalies += 1
        seen.append(row)
        
    print(f"Processed {len(rows)} employees.")
    print(f"Detected {anomalies} instances where the team composition deviated significantly from the historical norm.")
    print("Strategy: We monitor for statistical drift in 'YearsAtCompany+' and 'JobSatisfaction' "
          "using a 2-standard-deviation threshold to identify when a team no longer looks 'normal'.")
