import csv

def spot(header, rows):
    """
    Identifies rows that are 'suspicious' by looking for outliers in input columns.
    A row is suspicious if its input values are significantly far from the 
    median of that column (using a simple Z-score-like heuristic).
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Calculate medians for numeric inputs
    medians = {}
    for i in input_indices:
        vals = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if vals:
            vals.sort()
            medians[i] = vals[len(vals) // 2]

    # Score rows based on how many inputs are extreme outliers
    suspicion_scores = []
    for idx, row in enumerate(rows):
        score = 0
        for i in input_indices:
            val = row[i]
            if isinstance(val, (int, float)) and i in medians:
                # If value is more than 3x the median (or 0 if median is 0), flag it
                # This is a heuristic for "wrongly entered" data
                if medians[i] > 0 and (val > 10 * medians[i] or val < medians[i] / 10):
                    score += 1
        suspicion_scores.append((score, idx))

    # Sort by score descending
    suspicion_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return indices of rows with non-zero suspicion scores
    return [idx for score, idx in suspicion_scores if score > 0]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            data.append(processed_row)

    suspicious_indices = spot(header, data)
    
    print(f"Analysis complete. Found {len(suspicious_indices)} potentially erroneous rows.")
    if suspicious_indices:
        print("The 5 most suspicious row indices are:")
        print(suspicious_indices[:5])
    
    exit(0)
