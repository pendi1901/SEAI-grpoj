import csv

def spot(header, rows):
    """
    Identifies rows containing input values that are 'out of distribution'
    compared to the rest of the dataset. This detects settings the colleague
    might be suggesting that are far outside what has been tried.
    """
    # Identify input columns (those not ending in - or +)
    input_indices = [
        i for i, name in enumerate(header) 
        if not name.endswith('-') and not name.endswith('+')
    ]
    
    # Build a profile of known values for each input column
    # For numeric: range (min, max). For symbolic: set of seen values.
    profiles = {}
    for i in input_indices:
        col_data = [row[i] for row in rows if row[i] != "?"]
        if not col_data:
            continue
        
        if isinstance(col_data[0], (int, float)):
            profiles[i] = {'type': 'num', 'min': min(col_data), 'max': max(col_data)}
        else:
            profiles[i] = {'type': 'sym', 'seen': set(col_data)}
            
    # Score rows based on how many values fall outside the observed range/set
    suspicious = []
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if val == "?":
                continue
            
            p = profiles.get(i)
            if not p:
                continue
                
            if p['type'] == 'num':
                # If value is outside the min/max observed, it's suspicious
                if val < p['min'] or val > p['max']:
                    score += 1
            else:
                # If value is a category never seen before, it's suspicious
                if val not in p['seen']:
                    score += 1
        
        if score > 0:
            suspicious.append((idx, score))
            
    # Sort by score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[1], reverse=True)
    
    return [item[0] for item in suspicious]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)
            
    suspicious_indices = spot(header, rows)
    
    if not suspicious_indices:
        print("No suspicious settings found; all inputs are within observed ranges.")
    else:
        print(f"Found {len(suspicious_indices)} rows with settings outside observed ranges.")
        print("The most suspicious row indices are:")
        print(suspicious_indices[:10])
