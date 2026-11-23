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
        # we can simply sum the values (minimizing '-' and maximizing '+')
        total = 0
        for idx, op in goal_indices:
            val = float(row[idx])
            if op == '-':
                total += val
            else:
                total += (1.0 - val)
        return total

    # Score all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((score_row(row), i))

    # Sort by score (ascending, as we want lower values for '-' and higher for '+')
    scored.sort()

    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
        
        best_indices = remember(header, rows)
        
        print(f"Found {len(best_indices)} top-performing setups.")
        print("Indices of best rows:", best_indices)
        
        # Display a summary of the first best row
        if best_indices:
            idx = best_indices[0]
            print(f"\nExample of a top row (index {idx}):")
            for h, v in zip(header, rows[idx]):
                print(f"  {h}: {v}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
