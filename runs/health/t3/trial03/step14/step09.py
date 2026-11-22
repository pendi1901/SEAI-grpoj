import csv

def spot(header, rows):
    """
    Identifies rows that look like failed runs.
    A failed run often results in extreme outliers in the goal columns
    or inconsistent input values. We use Z-score analysis on the goal
    columns to find rows that are statistically anomalous.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Calculate anomaly score for each row based on goal metrics
    # We look for rows that are extreme outliers (Z-score > 3)
    anomaly_scores = []
    
    for i, row in enumerate(rows):
        score = 0
        for g_idx in goal_indices:
            val = row[g_idx]
            # Get column stats
            col_vals = [r[g_idx] for r in rows if isinstance(r[g_idx], (int, float))]
            if not col_vals:
                continue
            mean = sum(col_vals) / len(col_vals)
            std = (sum((x - mean)**2 for x in col_vals) / len(col_vals))**0.5
            if std > 0:
                z = abs(val - mean) / std
                score += z
        anomaly_scores.append((score, i))
    
    # Sort by anomaly score descending
    anomaly_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of rows with high anomaly scores (top 5%)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in anomaly_scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
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
    
    print("Analysis of potentially failed runs:")
    print(f"Identified {len(suspicious_indices)} rows that appear to be outliers or failed runs.")
    print("The 5 most suspicious row indices are:")
    print(suspicious_indices[:5])
