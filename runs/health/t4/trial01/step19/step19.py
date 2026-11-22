import csv

def spot(header, rows):
    """
    Identifies rows containing input values that are 'suspicious' or 'never seen'.
    We define 'never seen' as values outside the range observed in the training data.
    """
    # Identify input columns (all columns except the 3 goals)
    goal_indices = [0, 1, 2]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Build a profile of valid ranges/sets for each input column
    profiles = {}
    for i in input_indices:
        vals = [row[i] for row in rows if row[i] != "?"]
        if isinstance(vals[0], (int, float)):
            profiles[i] = (min(vals), max(vals))
        else:
            profiles[i] = set(vals)

    suspicious = []
    for row_idx, row in enumerate(rows):
        anomaly_score = 0
        for i in input_indices:
            val = row[i]
            if val == "?":
                continue
            
            # Check if value is outside observed range or set
            if isinstance(val, (int, float)):
                low, high = profiles[i]
                if val < low or val > high:
                    anomaly_score += 1
            else:
                if val not in profiles[i]:
                    anomaly_score += 1
        
        if anomaly_score > 0:
            suspicious.append((anomaly_score, row_idx))
    
    # Sort by anomaly score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    try:
                        processed.append(float(val))
                    except ValueError:
                        processed.append(0.0)
                else:
                    processed.append(val)
            rows.append(processed)

    suspicious_indices = spot(header, rows)
    
    print("Analysis complete.")
    if not suspicious_indices:
        print("No suspicious configurations found.")
    else:
        print(f"Identified {len(suspicious_indices)} configurations with values outside observed ranges.")
        print("Indices of the most suspicious rows (most anomalies first):")
        print(suspicious_indices[:10])
