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
        # Calculate a normalized score for each goal.
        # Since we want to find rows that are "unusually well", 
        # we look for rows that minimize the sum of normalized goal values.
        # For '-', we want low values. For '+', we want high values (so we use 1-val).
        total = 0.0
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
    
    # Sort by score ascending (lower is better)
    scored.sort()
    
    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
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
        
        # Display a summary of the first best row found
        if best_indices:
            print("\nExample of a top-performing row:")
            best_row = rows[best_indices[0]]
            for name, val in zip(header, best_row):
                print(f"  {name}: {val}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
