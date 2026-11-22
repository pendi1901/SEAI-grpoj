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
        # Since we want to be "unusually well" on all, we look for 
        # rows that are consistently low for '-' and high for '+'.
        # We use a simple heuristic: sum of normalized goal values.
        total = 0
        for idx, op in goal_indices:
            val = float(row[idx])
            total += val if op == '-' else (1.0 - val)
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
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            best_indices = remember(header, rows)
            
            print(f"Found {len(best_indices)} top-performing setups.")
            print("Indices of best rows:", best_indices)
            
            # Display the first best row as a sample
            if best_indices:
                print("\nSample of a top-performing row:")
                print(rows[best_indices[0]])
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
