import csv

def remember(header, rows):
    """
    Identifies the best rows based on multi-objective optimization.
    Goals: Minimize columns ending in '-', Maximize columns ending in '+'.
    Uses a simple Pareto-based ranking approach to find the 'handful' of best setups.
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    def is_better(row_a, row_b):
        # Returns True if row_a dominates or is better than row_b
        better_or_equal = True
        strictly_better = False
        for idx, direction in goals:
            val_a, val_b = row_a[idx], row_b[idx]
            if direction == 1:  # Maximize
                if val_a < val_b: return False
                if val_a > val_b: strictly_better = True
            else:  # Minimize
                if val_a > val_b: return False
                if val_a < val_b: strictly_better = True
        return strictly_better

    # Calculate a score based on how many other rows this row dominates
    # or simply rank by a weighted sum of normalized objectives.
    # Given the constraints, we pick the top 5% (40 rows out of 800).
    scores = []
    for i, row in enumerate(rows):
        # Normalize goals to [0, 1] range roughly
        score = 0
        for idx, direction in goals:
            # Simple heuristic: higher is better for the "trustworthiness" metric
            val = row[idx]
            score += val if direction == 1 else -val
        scores.append((score, i))
    
    scores.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (40 rows)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                # Convert numeric columns (upper case start)
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    best_indices = remember(header, rows)
    
    print(f"Found {len(best_indices)} unusually trustworthy setups.")
    print("Indices of top performing rows:", best_indices[:10], "...")
