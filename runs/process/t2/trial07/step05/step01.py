import csv

def remember(header, rows):
    """
    Identifies rows that perform well across all goal columns.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_row(row):
        # Calculate a normalized score for each goal
        # Since all data is numeric and normalized [0, 1], 
        # we can simply sum the values (inverted for '-')
        total = 0.0
        for idx, op in goal_indices:
            val = float(row[idx])
            if op == '-':
                total += val  # Lower is better
            else:
                total += (1.0 - val)  # Higher is better
        return total

    # Score all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((score_row(row), i))

    # Sort by score (ascending, as we want lower total penalty)
    scored.sort()

    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns to float
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    print(f"Found {len(best_indices)} top-performing setups.")
    print("Indices of best rows:", best_indices)
    print("\nSample of best row data:")
    for idx in best_indices[:3]:
        print(f"Row {idx}: {rows[idx]}")
