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
        # rows that are consistently low (for -) or high (for +).
        # We use the raw values since they are already in [0, 1].
        scores = []
        for idx, op in goal_indices:
            val = float(row[idx])
            scores.append(val if op == '-' else (1.0 - val))
        return sum(scores) / len(scores)

    # Calculate scores for all rows
    scored_rows = []
    for i, row in enumerate(rows):
        scored_rows.append((score_row(row), i))

    # Sort by score (ascending, as we want lower values for both '-' and inverted '+')
    scored_rows.sort()

    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored_rows[:limit]]

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
        
        # Display a summary of the first best row
        if best_indices:
            print("\nExample of a top-performing row:")
            best_row = rows[best_indices[0]]
            for h, v in zip(header, best_row):
                print(f"  {h}: {v}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
