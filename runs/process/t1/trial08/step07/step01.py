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
        # Calculate a normalized score for the row.
        # Since we want to minimize '-' and maximize '+', 
        # we can treat all as "minimize" by negating '+' values.
        # We use the raw values since they are already normalized [0, 1].
        total = 0
        for idx, sign in goal_indices:
            val = float(row[idx])
            total += val if sign == '-' else (1.0 - val)
        return total

    # Score all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((score_row(row), i))

    # Sort by score (ascending, as we minimized everything)
    scored.sort()

    # Return top 1% (or at least 1, max 5%)
    limit = max(1, len(rows) // 100)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    header = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                # Convert numeric columns to float, keep symbolic as is
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print(f"Found {len(best_indices)} top-performing setups.")
        print("Indices of best rows:", best_indices)
        for idx in best_indices:
            print(f"Row {idx}: {rows[idx]}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
