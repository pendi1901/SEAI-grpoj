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
        idx = header.index(col_name)
        low, high = bounds
        
        # Test 10 points across the allowed range
        for i in range(11):
            val = low + (high - low) * (i / 10.0)
            
            # Skip if it's the current value
            if abs(val - row[idx]) < 1e-9:
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
                rows.append([float(x) for x in row])

        # Levers based on the prompt: Plan and Team Size
        levers = {
            "Plan": (0.0, 1.0),
            "Team Size": (0.0, 1.0)
        }
        
        # Identify a bad row (high Cost- and high Idle-)
        cost_idx = header.index("Cost-")
        idle_idx = header.index("Idle-")
        bad_row = max(rows, key=lambda r: r[cost_idx] + r[idle_idx])
        
        changes = fix(header, bad_row, levers)
        
        print("Customer Inquiry: Rescue Plan")
        if changes:
            print("Analysis: To rescue the project, we recommend the following adjustment:")
            for col, val in changes.items():
                print(f"  - Adjust '{col}' to {val:.4f}")
        else:
            print("Analysis: No single lever adjustment was found to significantly improve performance.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
