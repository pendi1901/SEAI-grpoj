import csv

def remember(header, rows):
    """
    Identifies the best rows based on multi-objective optimization.
    Goals ending in '-' are minimized, '+' are maximized.
    We use the Pareto frontier concept: a row is 'unusually well' if 
    no other row is better in all goal dimensions.
    """
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goals.append((i, 1))   # Maximize

    def is_better(row_a, row_b):
        # Returns True if row_a dominates row_b
        better_in_at_least_one = False
        for idx, direction in goals:
            val_a = row_a[idx]
            val_b = row_b[idx]
            if direction == -1:  # Minimize
                if val_a > val_b: return False
                if val_a < val_b: better_in_at_least_one = True
            else:  # Maximize
                if val_a < val_b: return False
                if val_a > val_b: better_in_at_least_one = True
        return better_in_at_least_one

    # Find Pareto frontier
    pareto = []
    for i, row in enumerate(rows):
        is_dominated = False
        for j, other in enumerate(rows):
            if i == j: continue
            if is_better(other, row):
                is_dominated = True
                break
        if not is_dominated:
            pareto.append(i)
            
    # Return at most 5% of rows
    limit = max(1, len(rows) // 20)
    return pareto[:limit]

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                # Convert numeric columns to floats
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        best_indices = remember(header, rows)
        
        print(f"Found {len(best_indices)} unusually good setups (indices):")
        print(best_indices)
        
        # Print details for the first one as a sample
        if best_indices:
            print("\nSample of best setup:")
            print(dict(zip(header, rows[best_indices[0]])))
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
