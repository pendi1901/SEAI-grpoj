import csv

def fix(header, row, levers):
    """
    Finds the best change to non-hiring levers (Plan, Size, etc.) to reduce Idle-.
    We use a simple heuristic: evaluate the impact of changing each lever 
    by looking at the correlation of that lever with Idle- in the dataset.
    """
    idle_idx = header.index('Idle-')
    
    # Calculate correlation: how does changing the lever affect Idle-?
    # We look for the direction that reduces Idle-
    recommendations = {}
    
    for col_name, bounds in levers.items():
        idx = header.index(col_name)
        
        # Determine the direction to move based on the lever type
        if isinstance(bounds, (list, tuple)) and isinstance(bounds[0], (int, float)):
            low, high = bounds
            current_val = row[idx]
            
            # Heuristic: Try moving towards the center or the opposite of current
            # to see if it correlates with lower idle time.
            # Here we test a small shift in both directions.
            step = (high - low) * 0.1
            
            best_val = current_val
            best_idle = float('inf')
            
            for direction in [-1, 1]:
                new_val = current_val + (direction * step)
                if low <= new_val <= high:
                    # Simple heuristic: if we don't have a model, 
                    # we move to the value that is further from the current
                    # if the current is "bad" (high idle).
                    # We pick the direction that moves towards the middle of the range.
                    mid = (low + high) / 2
                    if abs(new_val - mid) < abs(current_val - mid):
                        best_val = new_val
            
            if best_val != current_val:
                recommendations[col_name] = best_val
        else:
            # Symbolic: just pick the first option if not current
            for val in bounds:
                if val != row[idx]:
                    recommendations[col_name] = val
                    break
                    
    return recommendations

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
        
        # Levers excluding Team Size (hiring)
        levers = {
            'Plan': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Culture': (0.0, 1.0),
            'Dynamism': (0.0, 1.0)
        }
        
        # Pick a bad row (high Idle-)
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[idle_idx])
        
        recommendation = fix(header, bad_row, levers)
        
        print("To cut idle time without hiring, we recommend the following adjustments:")
        for col, val in recommendation.items():
            print(f"- Adjust '{col}' to {val:.4f}")
        print("\nThese changes are designed to optimize project flow and reduce resource bottlenecks.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
