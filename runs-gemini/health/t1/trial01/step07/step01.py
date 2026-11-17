import csv

def remember(header, rows):
    """
    Identifies the best rows based on multi-objective optimization.
    Goals ending in '-' are minimized, '+' are maximized.
    We normalize numeric values to [0, 1] and use a simple distance metric
    to the ideal point (0 for '-', 1 for '+').
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, 'min'))
        elif name.endswith('+'):
            goals.append((i, 'max'))

    # Collect numeric data for normalization
    data = []
    for row in rows:
        clean_row = []
        for val in row:
            try:
                clean_row.append(float(val))
            except (ValueError, TypeError):
                clean_row.append(None)
        data.append(clean_row)

    # Find min/max for each goal column to normalize
    ranges = {}
    for idx, mode in goals:
        vals = [r[idx] for r in data if r[idx] is not None]
        if vals:
            ranges[idx] = (min(vals), max(vals))

    scores = []
    for i, row in enumerate(data):
        dist = 0
        count = 0
        for idx, mode in goals:
            val = row[idx]
            if val is not None and idx in ranges:
                low, high = ranges[idx]
                span = high - low if high > low else 1
                norm = (val - low) / span
                # If minimizing, ideal is 0. If maximizing, ideal is 1.
                dist += (norm if mode == 'min' else (1 - norm)) ** 2
                count += 1
        if count > 0:
            scores.append((dist / count, i))

    # Sort by distance (ascending) and return top 5% (or at least 1)
    scores.sort()
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)
    
    best_indices = remember(header, rows)
    
    print(f"Analysis complete. Found {len(best_indices)} trustworthy setups.")
    print("Top row indices:", best_indices)
    print("Example of best row (index {}): {}".format(best_indices[0], rows[best_indices[0]]))
