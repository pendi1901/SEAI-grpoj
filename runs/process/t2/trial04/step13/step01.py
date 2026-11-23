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
        # we can treat all as "minimize" by inverting '+' values.
        # Here we use a simple sum of normalized values.
        total = 0
        for idx, op in goal_indices:
            val = float(row[idx])
            total += val if op == '-' else (1.0 - val)
        return total

    # Score all rows
    scored = []
    for i, row in enumerate(rows):
        scored.append((score_row(row), i))
    
    # Sort by score ascending (lower is better)
    scored.sort()
    
    # Return top 5% (or at least 1)
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
                # Convert numeric columns to float, keep others as is
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print(f"Found {len(best_indices)} top-performing setups:")
        for idx in best_indices:
            # Print the goal values for the selected rows
            goals = {header[i]: rows[idx][i] for i, name in enumerate(header) 
                     if name.endswith('-') or name.endswith('+')}
            print(f"Row {idx}: {goals}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
