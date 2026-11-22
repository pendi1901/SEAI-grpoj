import csv

def spot(header, rows):
    """
    Identifies rows that contain input values that are statistically unlikely.
    We use the Interquartile Range (IQR) method on input columns to detect 
    outliers. A row is considered suspicious if its input values fall 
    outside the range [Q1 - 3*IQR, Q3 + 3*IQR].
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate bounds for each input column
    bounds = {}
    for i in input_indices:
        col_data = sorted([row[i] for row in rows if isinstance(row[i], (int, float))])
        if not col_data:
            continue
        q1 = col_data[len(col_data) // 4]
        q3 = col_data[3 * len(col_data) // 4]
        iqr = q3 - q1
        # Use a multiplier of 3.0 for "extreme" outliers
        bounds[i] = (q1 - 3.0 * iqr, q3 + 3.0 * iqr)
    
    # Score rows based on how many inputs fall outside bounds
    suspects = []
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if isinstance(val, (int, float)) and i in bounds:
                low, high = bounds[i]
                if val < low or val > high:
                    score += 1
        if score > 0:
            suspects.append((score, idx))
            
    # Sort by score descending (most suspicious first)
    suspects.sort(key=lambda x: x[0], reverse=True)
    return [idx for score, idx in suspects]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        suspect_indices = spot(header, rows)
        
        print("Analysis: Identifying unusual project setups.")
        if suspect_indices:
            print(f"Found {len(suspect_indices)} setups that contain input values unlike anything seen before.")
            print("The most suspicious row indices are:")
            print(suspect_indices[:10])
            print("\nThese rows contain input values that deviate significantly from historical norms.")
        else:
            print("No unusual setups were detected in the current dataset.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
