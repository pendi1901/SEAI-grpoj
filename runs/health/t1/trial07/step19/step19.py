import csv

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range
    (outliers). We calculate the range [min, max] for each numeric input
    and flag rows that contain values outside these bounds.
    """
    # Identify numeric input columns
    input_indices = [i for i, name in enumerate(header) 
                     if name in ['N_estimators', 'Min_sample_leaves', 
                                 'Min_impurity_decrease', 'Max_depth']]

    # Calculate bounds for each numeric input
    bounds = {}
    for idx in input_indices:
        vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        if vals:
            bounds[idx] = (min(vals), max(vals))

    # Score rows based on how many values are outside the observed range
    # or how far they deviate from the range.
    suspicion_scores = []
    for r_idx, row in enumerate(rows):
        score = 0
        for idx in input_indices:
            if idx in bounds and isinstance(row[idx], (int, float)):
                low, high = bounds[idx]
                # If value is outside the range, it is highly suspicious
                if row[idx] < low or row[idx] > high:
                    score += 10
                # Add a small penalty for being near the extreme
                else:
                    dist = min(abs(row[idx] - low), abs(row[idx] - high))
                    range_size = high - low
                    if range_size > 0:
                        score += (dist / range_size) * 0.1
        
        if score > 0:
            suspicion_scores.append((score, r_idx))

    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion_scores]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    suspicious_indices = spot(header, rows)
    
    print("Analysis: Identifying configurations that are 'far outside' our experience.")
    if not suspicious_indices:
        print("No suspicious configurations found; all inputs are within historical ranges.")
    else:
        print(f"Found {len(suspicious_indices)} rows with input values outside the observed range.")
        print("The most suspicious row indices are:", suspicious_indices[:5])
        print("\nThese rows contain settings that have never been tested before.")
        print("Proceed with caution when using these configurations.")
