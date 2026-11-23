import csv

def remember(header, rows):
    """
    Identifies the best-performing rows based on goal columns.
    Goals ending in '-' are minimized, '+' are maximized.
    Returns the indices of the top 1% (or at least 1, max 5%) of rows.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_row(row):
        # Normalize goals: minimize '-' and maximize '+' (1 - val)
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
    try:
        rows = []
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
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print("Analysis: Identifying historical setups that performed best.")
        print(f"Found {len(best_indices)} top-performing historical configurations.")
        print("These setups represent the most efficient outcomes in our dataset.")
        print("Indices of best rows:", best_indices)
        
        # Display the first best row as an example
        if best_indices:
            idx = best_indices[0]
            print(f"\nExample of a top-performing setup (Row {idx}):")
            for name, val in zip(header, rows[idx]):
                print(f"  {name}: {val}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
