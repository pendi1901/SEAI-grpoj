import csv

def spot(header, rows):
    """
    Identifies rows containing input values that are 'far outside' the 
    observed range of the training data (outliers).
    
    We define 'suspicious' as having input values that fall outside 
    the min/max range observed in the majority of the data.
    """
    input_indices = [i for i, h in enumerate(header) if not h.endswith(('-', '+'))]
    
    # Calculate bounds for each numeric input column
    bounds = {}
    for i in input_indices:
        if header[i] == 'criterion':
            continue
        col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if col_vals:
            bounds[i] = (min(col_vals), max(col_vals))

    suspicious = []
    for row_idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            if i in bounds:
                val = row[i]
                mn, mx = bounds[i]
                # If a value is outside the observed range, it's suspicious
                if val < mn or val > mx:
                    score += 1
        
        if score > 0:
            suspicious.append((score, row_idx))
    
    # Sort by score (number of out-of-bounds inputs) descending
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] == 'criterion':
                        processed_row.append(val)
                    else:
                        processed_row.append(float(val))
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print(f"Identified {len(suspicious_indices)} rows with potentially invalid/out-of-range settings.")
        print("Top 5 most suspicious row indices:")
        for idx in suspicious_indices[:5]:
            print(f"Row {idx}: {rows[idx]}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
