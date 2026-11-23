import csv

def spot(header, rows):
    """
    Identifies rows that are 'outliers' based on input values.
    Since the data is normalized [0, 1], any value outside this range is 
    highly suspicious. Additionally, we calculate the distance of each row 
    from the centroid of the data to find rows that are statistically unusual.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    suspicious = []
    
    # 1. Check for values outside [0, 1] (Data entry errors)
    for i, row in enumerate(rows):
        for idx in input_indices:
            try:
                val = float(row[idx])
                if val < 0 or val > 1:
                    # Assign a high score for out-of-bounds values
                    suspicious.append((10.0, i))
                    break
            except (ValueError, TypeError):
                continue
    
    # 2. Check for statistical outliers (rows far from the mean)
    # Calculate column means
    means = []
    for idx in input_indices:
        vals = [float(r[idx]) for r in rows if r[idx] != "?"]
        if vals:
            means.append(sum(vals) / len(vals))
        else:
            means.append(0.5)
    
    # Calculate distance from centroid
    for i, row in enumerate(rows):
        d = 0
        count = 0
        for j, idx in enumerate(input_indices):
            if row[idx] != "?":
                d += (float(row[idx]) - means[j]) ** 2
                count += 1
        if count > 0:
            dist = (d / count) ** 0.5
            # Only add if not already flagged as highly suspicious
            if not any(idx == i for score, idx in suspicious):
                suspicious.append((dist, i))
        
    # Sort by suspicion score (descending)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    
    return [i for score, i in suspicious]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
        
        outliers = spot(header, rows)
        
        print("Customer Inquiry: Identifying setups never seen before (outliers)")
        print("-" * 60)
        if outliers:
            print(f"Found {len(outliers)} suspicious or unique configurations.")
            print("The most suspicious row indices (most unique/erroneous) are:")
            print(outliers[:10])
            print("\nThese rows contain values that deviate significantly from the norm")
            print("or fall outside the expected [0, 1] range.")
        else:
            print("No suspicious records found.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
