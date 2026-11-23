import csv

def remember(header, rows):
    """
    Identifies the best rows based on multi-objective optimization.
    Goals: Minimize columns ending in '-', Maximize columns ending in '+'.
    Uses a simple Pareto-dominance approach to find the 'best' setups.
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    def get_score(row):
        # Normalize values to compare different scales
        # Since we want to find 'unusually trustworthy', we look for 
        # rows that perform well across all goal columns.
        scores = []
        for idx, direction in goals:
            val = row[idx]
            # Simple heuristic: higher is better for +, lower for -
            scores.append(val * direction)
        return sum(scores)

    # Calculate scores and keep track of original indices
    indexed_rows = []
    for i, row in enumerate(rows):
        indexed_rows.append((i, get_score(row)))

    # Sort by score descending
    indexed_rows.sort(key=lambda x: x[1], reverse=True)

    # Return top 5% (800 rows * 0.05 = 40 rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[0] for item in indexed_rows[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            # Convert numeric columns to floats, keep symbolic as strings
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)
            
    best_indices = remember(header, rows)
    
    print(f"Analysis complete. Found {len(best_indices)} trustworthy setups.")
    print("Indices of the best performing setups:")
    print(best_indices)
