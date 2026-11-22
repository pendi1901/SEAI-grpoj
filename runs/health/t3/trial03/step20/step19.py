import csv

def spot(header, rows):
    """
    Identifies rows containing input values that are 'out of distribution'
    compared to the rest of the dataset. We use a simple range-based check
    for numeric inputs and a frequency-based check for symbolic inputs.
    """
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate bounds for numeric and frequencies for symbolic
    stats = {}
    for i in input_indices:
        col_vals = [row[i] for row in rows if row[i] != "?"]
        if not col_vals:
            continue
        
        if isinstance(col_vals[0], (int, float)):
            stats[i] = {'type': 'num', 'min': min(col_vals), 'max': max(col_vals)}
        else:
            # Frequency map
            counts = {}
            for v in col_vals:
                counts[v] = counts.get(v, 0) + 1
            stats[i] = {'type': 'sym', 'freq': counts}

    suspicious = []
    for r_idx, row in enumerate(rows):
        anomaly_score = 0
        for i in input_indices:
            val = row[i]
            if val == "?":
                continue
            
            s = stats.get(i)
            if not s:
                continue
                
            if s['type'] == 'num':
                # If value is outside the observed range, it's highly suspicious
                if val < s['min'] or val > s['max']:
                    anomaly_score += 10
            else:
                # If value is a category never seen before, it's suspicious
                if val not in s['freq']:
                    anomaly_score += 10
        
        if anomaly_score > 0:
            suspicious.append((anomaly_score, r_idx))
            
    # Sort by score descending
    suspicious.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
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
    
    print("Analysis of unusual configurations:")
    if not suspicious_indices:
        print("No suspicious configurations found. All inputs are within expected ranges.")
    else:
        print(f"Identified {len(suspicious_indices)} rows with values outside the observed training distribution.")
        print("The 5 most suspicious row indices are:")
        print(suspicious_indices[:5])
