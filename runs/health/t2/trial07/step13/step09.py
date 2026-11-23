import csv
import step01

def spot(header, rows):
    """
    Identifies suspicious rows (outliers) based on input feature distributions.
    Rows with values significantly outside the range of other rows for 
    numeric inputs are flagged as suspicious.
    """
    # Identify input columns (non-goal columns)
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Calculate stats for numeric inputs to find outliers
    stats = {}
    for i in input_indices:
        if isinstance(rows[0][i], float):
            vals = [r[i] for r in rows if r[i] != "?"]
            if not vals: continue
            mean = sum(vals) / len(vals)
            std = (sum((x - mean)**2 for x in vals) / len(vals))**0.5
            stats[i] = (mean, std)

    scores = []
    for row_idx, row in enumerate(rows):
        suspicion = 0
        for i in input_indices:
            if i in stats and row[i] != "?":
                mean, std = stats[i]
                if std > 0:
                    # Z-score based suspicion
                    z = abs(row[i] - mean) / std
                    if z > 3:  # Threshold for outlier
                        suspicion += z
        if suspicion > 0:
            scores.append((suspicion, row_idx))
    
    # Sort by suspicion descending
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        suspicious_indices = spot(header, rows)
        
        print("Suspicious rows identified (most suspicious first):")
        # Print top 10 for brevity
        for idx in suspicious_indices[:10]:
            print(f"Row {idx} is highly suspicious.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
