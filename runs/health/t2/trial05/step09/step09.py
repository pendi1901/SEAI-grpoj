import csv

def spot(header, rows):
    """
    Identifies suspicious rows (outliers).
    A row is suspicious if its input values are significantly distant 
    from the median of the dataset (using a simple Z-score-like heuristic).
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate medians for numeric inputs
    medians = {}
    for i in input_indices:
        if isinstance(rows[0][i], float):
            vals = sorted([r[i] for r in rows if r[i] != "?"])
            medians[i] = vals[len(vals) // 2] if vals else 0.0

    scores = []
    for idx, row in enumerate(rows):
        # Calculate anomaly score: sum of squared deviations from median
        anomaly_score = 0.0
        for i in input_indices:
            if isinstance(row[i], float) and row[i] != "?":
                # Normalize deviation by median (simple outlier detection)
                if medians[i] != 0:
                    anomaly_score += abs(row[i] - medians[i]) / medians[i]
        scores.append((anomaly_score, idx))
    
    # Sort by anomaly score descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 10 most suspicious indices
    return [item[1] for item in scores[:10]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        suspicious = spot(header, rows)
        
        print("The most suspicious rows (potential failed runs) are:")
        for idx in suspicious[:5]:
            print(f"Row {idx}: MRE={rows[idx][0]:.4f}, ACC={rows[idx][1]:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
