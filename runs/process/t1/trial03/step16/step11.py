import csv

def remember(header, rows):
    """
    Identifies the best rows based on goal minimization/maximization.
    Goals ending in '-' are minimized, '+' are maximized.
    Returns the indices of the top 5% of rows.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))

    def get_score(row):
        # Normalize: minimize all.
        # For '-', lower is better. For '+', higher is better (so negate).
        score = 0
        for idx, op in goal_indices:
            val = float(row[idx])
            score += val if op == '-' else -val
        return score

    # Calculate scores for all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((get_score(row), i))

    # Sort by score (ascending, as lower is better)
    scored.sort()

    # Return the top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print("Analysis: Identifying top-performing project configurations.")
        print(f"Found {len(best_indices)} configurations that represent the best outcomes.")
        print("\nTop 3 best-performing rows (indices):")
        for idx in best_indices[:3]:
            row = rows[idx]
            goals = {header[i]: row[i] for i, name in enumerate(header) 
                     if name.endswith('-') or name.endswith('+')}
            print(f"Index {idx}: {goals}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
