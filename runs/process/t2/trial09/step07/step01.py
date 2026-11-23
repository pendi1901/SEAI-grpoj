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
        # we can treat all goals as "minimize" by negating '+' values.
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
    
    # Sort by score (ascending, as we minimized everything)
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
            rows = [row for row in reader]
            
            # Convert numeric columns to floats
            for row in rows:
                for i in range(len(row)):
                    try:
                        row[i] = float(row[i])
                    except ValueError:
                        pass
            
            best_indices = remember(header, rows)
            
            print(f"Found {len(best_indices)} top-performing setups.")
            print("Indices of best rows:", best_indices)
            
            # Print a summary of the first best row
            if best_indices:
                idx = best_indices[0]
                print(f"\nExample of a top row (index {idx}):")
                for name, val in zip(header, rows[idx]):
                    print(f"  {name}: {val}")
                    
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
