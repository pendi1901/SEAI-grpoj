import csv

def spot(header, rows):
    """
    Identifies rows that contain input values far outside the observed range 
    or rare symbolic categories, suggesting they are 'wrong' or 'unseen'.
    """
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    # Calculate bounds for numeric inputs and frequency for symbolic inputs
    stats = {}
    for i in input_indices:
        col_data = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if col_data:
            mn, mx = min(col_data), max(col_data)
            # Use a buffer to define "far outside"
            rng = mx - mn
            stats[i] = (mn - 0.5 * rng, mx + 0.5 * rng)
        else:
            # Symbolic: track frequency
            col_vals = [r[i] for r in rows]
            counts = {}
            for v in col_vals:
                counts[v] = counts.get(v, 0) + 1
            stats[i] = counts

    suspicion_scores = []
    for row_idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if isinstance(val, (int, float)) and i in stats:
                mn, mx = stats[i]
                if val < mn or val > mx:
                    score += 5.0  # High penalty for out-of-bounds
            elif isinstance(val, str):
                counts = stats[i]
                freq = counts[val] / len(rows)
                if freq < 0.01:  # Very rare category
                    score += 3.0
        
        if score > 0:
            suspicion_scores.append((score, row_idx))

    # Sort by suspicion score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    return [item[1] for item in suspicion_scores]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['criterion']:
                        processed.append(val)
                    else:
                        processed.append(float(val))
                rows.append(processed)
        
        suspicious = spot(header, rows)
        
        if not suspicious:
            print("No suspicious or 'unseen' configurations detected.")
        else:
            print(f"Detected {len(suspicious)} configurations that contain settings far outside historical norms.")
            print("The most suspicious row indices are:")
            print(suspicious[:10])
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
