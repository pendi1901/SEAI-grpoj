import csv

def remember(header, rows):
    """
    Identifies rows that perform well across all goal columns.
    Goals ending in '-' are minimized, '+' are maximized.
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goals.append((i, name.endswith('-')))

    # Calculate a score for each row based on the normalized rank of its goals.
    # Since all goals are numeric and in [0, 1], we can simply sum the 
    # normalized values (minimizing '-' is equivalent to maximizing 1 - value).
    scores = []
    for idx, row in enumerate(rows):
        total_score = 0
        for col_idx, is_min in goals:
            val = float(row[col_idx])
            total_score += (1.0 - val) if is_min else val
        scores.append((total_score, idx))

    # Sort by total score descending (best performers first)
    scores.sort(key=lambda x: x[0], reverse=True)

    # Return top 5% (or at least 1)
    limit = max(1, len(rows) // 20)
    return [item[1] for item in scores[:limit]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to float, keep symbolic as strings
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
            goal_vals = [f"{header[i]}={rows[idx][i]:.4f}" 
                         for i, name in enumerate(header) 
                         if name.endswith('-') or name.endswith('+')]
            print(f"Row {idx}: {', '.join(goal_vals)}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
