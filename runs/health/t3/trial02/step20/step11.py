import csv

def remember(header, rows):
    """
    Identifies the best rows by calculating a normalized score for each row
    based on the goal columns (MRE-, ACC+, PRED40+).
    Returns the indices of the top 5% of rows.
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    # Calculate normalized scores
    scores = [0.0] * len(rows)
    for col_idx, direction in goals:
        values = [row[col_idx] for row in rows]
        min_v, max_v = min(values), max(values)
        rng = max_v - min_v if max_v != min_v else 1.0
        
        for r_idx, row in enumerate(rows):
            val = (row[col_idx] - min_v) / rng
            if direction == -1:
                val = 1.0 - val
            scores[r_idx] += val

    # Get indices of top 5%
    num_to_return = max(1, len(rows) // 20)
    indexed_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    
    return [x[0] for x in indexed_scores[:num_to_return]]

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
    
    best_indices = remember(header, rows)
    
    print("Top performing setups identified:")
    for idx in best_indices:
        row = rows[idx]
        # Extract goals for display
        goals = {header[i]: row[i] for i, h in enumerate(header) if h.endswith(('-', '+'))}
        print(f"Row {idx}: {goals}")
