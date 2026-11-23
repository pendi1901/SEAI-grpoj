import csv

def flow(header, row, seen):
    """
    Detects if a team's composition has drifted significantly from the norm.
    We monitor the mean of 'YearsAtCompany+' (a goal to maximize).
    If the current row's value is more than 2 standard deviations away 
    from the mean of the 'seen' data, we flag it as an anomaly.
    """
    # Identify goal column
    try:
        goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    except StopIteration:
        return False

    # Need a baseline to detect drift
    if len(seen) < 30:
        return False

    # Calculate statistics of seen data
    values = [r[goal_idx] for r in seen]
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std_dev = variance ** 0.5

    # If std_dev is 0, we can't detect drift via this method
    if std_dev == 0:
        return False

    # Check if the current row is an outlier (drift)
    current_val = row[goal_idx]
    z_score = abs(current_val - mean) / std_dev

    # If z-score > 2, the team composition looks different (anomaly)
    return z_score > 2.0

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
        
    print("Team Drift Analysis:")
    print(f"Total records processed: {len(rows)}")
    print(f"Number of times the team composition deviated significantly: {anomalies}")
    print("Strategy: Flagging rows where 'YearsAtCompany+' deviates by more than 2 standard deviations from the historical mean.")
