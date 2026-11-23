import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by detecting outliers in the input 
    columns. A row is considered suspicious if its input values are 
    statistically distant from the median of the dataset.
    """
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Calculate medians for numeric inputs to detect outliers
    medians = {}
    for i in input_indices:
        if isinstance(rows[0][i], float):
            vals = sorted([r[i] for r in rows])
            medians[i] = vals[len(vals) // 2]
    
    suspicious = []
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if isinstance(val, float) and i in medians:
                # Simple outlier detection: distance from median
                # We use absolute difference as a proxy for "wrongly entered"
                score += abs(val - medians[i])
            elif isinstance(val, str):
                # For symbolic, check if it's a rare category
                col_vals = [r[i] for r in rows]
                if col_vals.count(val) < len(rows) * 0.05:
                    score += 1.0
        
        if score > 0:
            suspicious.append((score, idx))
    
    # Sort by score descending (most suspicious first)
    suspicious.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in suspicious]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    suspicious_indices = spot(header, rows)
    
    print("Analysis complete. Identified potentially failed/erroneous runs.")
    print(f"Found {len(suspicious_indices)} suspicious rows.")
    print("Top 5 most suspicious row indices:")
    print(suspicious_indices[:5])
    
    print("\nDetails of the most suspicious row:")
    top_idx = suspicious_indices[0]
    print(f"Row {top_idx}: {rows[top_idx]}")
