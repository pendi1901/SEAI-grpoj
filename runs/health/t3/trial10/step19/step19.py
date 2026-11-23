import csv

def spot(header, rows):
    """
    Identifies rows containing input values that are 'far outside' 
    the range of values seen in the rest of the dataset.
    
    We calculate the range [min, max] for each numeric input column 
    and flag rows that contain values outside these bounds.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Identify numeric input columns
    numeric_inputs = [i for i in input_indices if isinstance(rows[0][i], (int, float))]
    
    # Calculate bounds for each numeric input
    bounds = {}
    for i in numeric_inputs:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if vals:
            bounds[i] = (min(vals), max(vals))
            
    # Score rows based on how many values are outside the observed range
    # (or if a value is extremely far from the mean)
    suspicion_scores = []
    for row_idx, row in enumerate(rows):
        score = 0
        for i in numeric_inputs:
            val = row[i]
            if isinstance(val, (int, float)):
                mn, mx = bounds[i]
                # If value is outside the range, it's highly suspicious
                if val < mn or val > mx:
                    score += 10
                # Also check for values that are statistically extreme (Z-score > 3)
                col_vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
                mu = sum(col_vals) / len(col_vals)
                sigma = (sum((x - mu) ** 2 for x in col_vals) / len(col_vals)) ** 0.5
                if sigma > 0 and abs(val - mu) / sigma > 3:
                    score += 1
        suspicion_scores.append((score, row_idx))
    
    # Sort by score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return only rows with a non-zero suspicion score
    return [idx for score, idx in suspicion_scores if score > 0]

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
    
    print("Analysis complete: Identified rows with settings far outside historical norms.")
    if suspicious_indices:
        print(f"Found {len(suspicious_indices)} suspicious rows.")
        print(f"Top 5 most suspicious row indices: {suspicious_indices[:5]}")
    else:
        print("No suspicious rows found.")
    
    exit(0)
