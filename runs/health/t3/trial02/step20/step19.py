import csv

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range
    (outliers). We use the Interquartile Range (IQR) method to detect values
    that are statistically 'unseen' or extreme compared to the rest of the data.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Only consider numeric input columns for outlier detection
    numeric_inputs = {}
    for idx in input_indices:
        vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        if vals:
            vals.sort()
            q1 = vals[len(vals) // 4]
            q3 = vals[3 * len(vals) // 4]
            iqr = q3 - q1
            # Define bounds: anything outside 1.5 * IQR is suspicious
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            numeric_inputs[idx] = (lower_bound, upper_bound)

    suspicion_scores = [0.0] * len(rows)
    
    for idx, (low, high) in numeric_inputs.items():
        for r_idx, row in enumerate(rows):
            val = row[idx]
            if isinstance(val, (int, float)):
                # Score based on how far outside the bounds the value is
                if val < low:
                    suspicion_scores[r_idx] += (low - val)
                elif val > high:
                    suspicion_scores[r_idx] += (val - high)

    # Sort rows by suspicion score descending
    indexed_scores = sorted(enumerate(suspicion_scores), key=lambda x: x[1], reverse=True)
    
    # Return indices of rows with non-zero suspicion
    return [i for i, score in indexed_scores if score > 0]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    suspicious_indices = spot(header, rows)
    
    print(f"Analysis complete. Found {len(suspicious_indices)} rows with settings far outside observed ranges.")
    if suspicious_indices:
        print(f"The most suspicious row index is {suspicious_indices[0]}.")
        print(f"Data for that row: {rows[suspicious_indices[0]]}")
    else:
        print("No suspicious (outlier) settings detected.")
