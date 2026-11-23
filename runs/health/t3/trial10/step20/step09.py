import csv

def spot(header, rows):
    """
    Identifies rows that look like failed runs.
    A failed run often manifests as extreme outliers in input parameters
    or inconsistent behavior relative to the rest of the dataset.
    We use Z-score analysis on numeric inputs to find suspicious rows.
    """
    # Identify input indices (non-goal columns)
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Calculate Z-scores for numeric inputs
    # A row is suspicious if it has extreme values (high Z-score)
    suspicion_scores = [0.0] * len(rows)
    
    for i in input_indices:
        # Only process numeric columns
        if isinstance(rows[0][i], (int, float)):
            col_vals = [r[i] for r in rows]
            mu = sum(col_vals) / len(col_vals)
            sigma = (sum((x - mu) ** 2 for x in col_vals) / len(col_vals)) ** 0.5
            
            if sigma > 0:
                for row_idx, row in enumerate(rows):
                    z = abs(row[i] - mu) / sigma
                    suspicion_scores[row_idx] += z
                    
    # Sort indices by suspicion score descending
    indexed_scores = list(enumerate(suspicion_scores))
    indexed_scores.sort(key=lambda x: x[1], reverse=True)
    
    return [idx for idx, score in indexed_scores if score > 0]

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
    
    print("Analysis complete. Identified potentially failed runs.")
    print(f"Top 5 most suspicious row indices: {suspicious_indices[:5]}")
    
    exit(0)
