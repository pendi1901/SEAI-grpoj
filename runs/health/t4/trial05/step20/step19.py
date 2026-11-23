import csv

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range 
    (potential data entry errors).
    
    Logic:
    1. Identify input columns (all except goals).
    2. For numeric inputs, calculate the min and max observed in the dataset.
    3. A row is suspicious if any of its input values fall significantly 
       outside the range [min, max] of the rest of the data.
    """
    goal_names = ['MRE-', 'ACC+', 'PRED40+']
    input_indices = [i for i, name in enumerate(header) if name not in goal_names]
    
    # Calculate bounds for numeric inputs
    numeric_indices = [i for i in input_indices if not isinstance(rows[0][i], str)]
    bounds = {}
    for i in numeric_indices:
        vals = [r[i] for r in rows if r[i] is not None]
        bounds[i] = (min(vals), max(vals))
    
    suspicious = []
    for idx, row in enumerate(rows):
        score = 0
        for i in numeric_indices:
            val = row[i]
            low, high = bounds[i]
            # If a value is outside the observed range, it is suspicious
            if val < low or val > high:
                score += 1
        
        if score > 0:
            suspicious.append((score, idx))
    
    # Sort by number of suspicious features descending
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
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
    
    print("Customer Inquiry: Are there settings outside of what we have tried?")
    if not suspicious_indices:
        print("No suspicious rows found; all inputs are within observed ranges.")
    else:
        print(f"Found {len(suspicious_indices)} rows with inputs outside the normal range.")
        print("Top 5 most suspicious row indices:", suspicious_indices[:5])
    
    exit(0)
