import csv

def get_score(header, row):
    """Calculates a normalized score [0, 1] where lower is better."""
    goal_indices = []
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_indices.append((i, name[-1]))
    
    scores = []
    for idx, op in goal_indices:
        val = float(row[idx])
        scores.append(val if op == '-' else (1.0 - val))
    return sum(scores) / len(scores)

def fix(header, row, levers):
    """
    Finds the best single-lever change that improves the row's score.
    """
    best_score = get_score(header, row)
    best_change = {}
    
    for col_name, bounds in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        
        # Determine test values based on type
        if isinstance(bounds, (list, tuple)) and not isinstance(bounds[0], (int, float)):
            # Symbolic column
            test_values = bounds
        else:
            # Numeric column (low, high)
            low, high = bounds
            test_values = [low + (high - low) * (i / 10.0) for i in range(11)]
            
        for val in test_values:
            # Skip if it's the current value
            if isinstance(val, (int, float)) and abs(val - float(row[idx])) < 1e-9:
                continue
            if val == row[idx]:
                continue
                
            test_row = list(row)
            test_row[idx] = val
            
            score = get_score(header, test_row)
            if score < best_score:
                best_score = score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    try:
                        processed.append(float(val))
                    except ValueError:
                        processed.append(val)
                rows.append(processed)

        # Customer cannot hire (Team Size is fixed).
        # We offer other levers: Culture, Plan, and Size.
        levers = {
            "Culture": (0.0, 1.0),
            "Plan": (0.0, 1.0),
            "Size": (0.0, 1.0)
        }
        
        # Identify a bad row (high Idle-)
        idle_idx = header.index("Idle-")
        bad_row = max(rows, key=lambda r: r[idle_idx])
        
        changes = fix(header, bad_row, levers)
        
        print("Customer Inquiry: Reducing Idle Time without Hiring")
        if changes:
            print("Analysis: To reduce idle time, we recommend the following adjustment:")
            for col, val in changes.items():
                if isinstance(val, (int, float)):
                    print(f"  - Adjust '{col}' to {val:.4f}")
                else:
                    print(f"  - Adjust '{col}' to {val}")
        else:
            print("Analysis: No single lever adjustment was found to significantly improve idle time.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
