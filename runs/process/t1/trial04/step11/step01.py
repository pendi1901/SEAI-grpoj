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
    # Since all goals are numeric and in [0, 1], we can use the values directly.
    # For minimization (-), lower is better. For maximization (+), higher is better.
    # We want to minimize (value) for '-' and minimize (1 - value) for '+'.
    
    scored_rows = []
    for idx, row in enumerate(rows):
        total_penalty = 0
        for col_idx, is_min in goals:
            val = float(row[col_idx])
            if is_min:
                total_penalty += val
            else:
                total_penalty += (1.0 - val)
        scored_rows.append((total_penalty, idx))
    
    # Sort by total penalty (ascending)
    scored_rows.sort()
    
    # Return the top 5% of rows (or at least 1)
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
                # Convert numeric columns to float, keep symbolic as strings
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
        
        # Print a summary of the first best row found
        if best_indices:
            print("\nExample of a top-performing row:")
            first_best = rows[best_indices[0]]
            for h, v in zip(header, first_best):
                print(f"  {h}: {v}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
