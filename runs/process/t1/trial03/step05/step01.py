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
        # We want to minimize all goals. 
        # For '-', lower is better. For '+', higher is better (so we negate).
        scores = []
        for idx, op in goal_indices:
            val = float(row[idx])
            scores.append(val if op == '-' else -val)
        return scores

    # Calculate scores for all rows
    scored_rows = []
    for i, row in enumerate(rows):
        scored_rows.append((score_row(row), i))

    # Sort by the goals lexicographically (all goals are equally important)
    scored_rows.sort()

    # Return the top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scored_rows[:limit]]

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
        
        print(f"Found {len(best_indices)} top-performing setups.")
        print("Indices of best rows:", best_indices)
        
        # Print a summary of the first best row
        if best_indices:
            print("\nExample of a top-performing row (index {}):".format(best_indices[0]))
            print(dict(zip(header, rows[best_indices[0]])))
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
