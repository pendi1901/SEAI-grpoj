import csv

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range 
    of the training data. Returns the indices of these rows, sorted by 
    suspicion score (descending).
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate bounds for numeric inputs
    bounds = {}
    for i in input_indices:
        col_data = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if col_data:
            mn, mx = min(col_data), max(col_data)
            # Define a buffer (e.g., 20% of range) to identify "far outside"
            rng = mx - mn
            if rng > 0:
                bounds[i] = (mn - 0.2 * rng, mx + 0.2 * rng)
            else:
                bounds[i] = (mn, mx)

    suspicious = []
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if isinstance(val, (int, float)) and i in bounds:
                mn, mx = bounds[i]
                # If value is outside the observed range, increase suspicion
                if val < mn or val > mx:
                    score += 1
            elif isinstance(val, str):
                # Check for unknown symbolic values if necessary
                # (Assuming standard categories are known from the dataset)
                pass
        
        if score > 0:
            suspicious.append((score, idx))

    # Sort by suspicion score descending
    suspicious.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        anomalies = spot(header, rows)
        
        if anomalies:
            print(f"Detected {len(anomalies)} rows with settings far outside observed ranges.")
            print("The most suspicious row indices are:", anomalies[:5])
        else:
            print("No anomalous settings detected.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
