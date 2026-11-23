import csv

def remember(header, rows):
    """
    Identifies the best rows based on multi-objective optimization.
    A row is 'unusually well' if no other row is better in all goal dimensions.
    Returns the indices of the Pareto frontier, limited to 5% of the total rows.
    """
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goal_indices.append((i, -1))  # Minimize
        elif name.endswith('+'):
            goal_indices.append((i, 1))   # Maximize

    def is_better(row_a, row_b):
        # Returns True if row_a dominates row_b
        better_in_at_least_one = False
        for idx, direction in goal_indices:
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

def load_data(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            processed = []
            for val in row:
                try:
                    processed.append(float(val))
                except ValueError:
                    processed.append(val)
            rows.append(processed)
    return header, rows

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        header, rows = load_data(filename)
        best_indices = remember(header, rows)
        
        print(f"Analysis complete. Found {len(best_indices)} configurations that represent the Pareto frontier.")
        print("These configurations are the most balanced, offering the best trade-offs between cost, score, and idle time.")
        print(f"Indices of the best setups: {best_indices}")
        
        if best_indices:
            sample_idx = best_indices[0]
            print(f"\nSample of a top-performing setup (Index {sample_idx}):")
            goal_names = [name for name in header if name.endswith(('-', '+'))]
            for name in goal_names:
                idx = header.index(name)
                print(f"  {name}: {rows[sample_idx][idx]:.4f}")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
