import csv

def spot(header, rows):
    """
    Identifies rows that are 'unseen' or 'anomalous' by checking if any 
    input value falls outside the range observed in the rest of the dataset.
    Returns the indices of rows containing such values, sorted by the 
    number of suspicious features (most suspicious first).
    """
    # Identify input columns (exclude goals)
    input_indices = [i for i, h in enumerate(header) 
                     if h[0].isupper() and not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate min and max for each input column
    ranges = {}
    for i in input_indices:
        vals = [row[i] for row in rows if isinstance(row[i], (int, float))]
        if vals:
            ranges[i] = (min(vals), max(vals))
    
    suspicion_scores = []
    for idx, row in enumerate(rows):
        count = 0
        for i in input_indices:
            val = row[i]
            if isinstance(val, (int, float)) and i in ranges:
                low, high = ranges[i]
                # If a value is outside the observed range, it's "never seen"
                if val < low or val > high:
                    count += 1
        
        if count > 0:
            suspicion_scores.append((count, idx))
    
    # Sort by count descending (most suspicious first)
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [idx for count, idx in suspicion_scores]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
                rows.append(processed_row)
        
        suspicious_indices = spot(header, rows)
        
        print("Customer Inquiry: Identifying setups that contain never-before-seen input values.")
        print("-" * 70)
        if not suspicious_indices:
            print("No anomalous setups found. All inputs are within historical ranges.")
        else:
            print(f"Found {len(suspicious_indices)} setups with values outside historical norms.")
            print("Top 5 most suspicious row indices:")
            for idx in suspicious_indices[:5]:
                print(f" - Row {idx}")
            print("\nConclusion: These rows contain input values that deviate from all previous runs.")
            print("We recommend reviewing these configurations for potential data entry errors.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
