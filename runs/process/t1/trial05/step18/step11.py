import csv

def remember(header, rows):
    """
    Identifies the top 5% of rows based on goal optimization.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def score_row(row):
        # Normalize goals to [0, 1] range and sum them
        # Since data is already normalized [0, 1], we just aggregate
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

    # Sort by score (ascending: lower is better)
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
        
        print("Customer Inquiry: Show me the past setups most like the best ones.")
        print("-" * 60)
        print(f"Found {len(best_indices)} top-performing historical configurations.")
        print("Indices of the best historical rows:", best_indices[:10], "..." if len(best_indices) > 10 else "")
        
        if best_indices:
            idx = best_indices[0]
            print(f"\nExample of a top-performing historical setup (index {idx}):")
            for h, v in zip(header, rows[idx]):
                print(f"  {h}: {v}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
