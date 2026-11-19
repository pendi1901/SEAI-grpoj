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
    Finds the smallest change to levers that improves the row's score.
    We perform a local search by trying small adjustments to each lever.
    """
    best_row = list(row)
    best_score = get_score(header, row)
    recommendations = {}

    for col_name, bounds in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try a few steps within the allowed range
        low, high = bounds
        # Create 5 test points in the range
        steps = [low + (high - low) * (i / 4.0) for i in range(5)]
        
        for val in steps:
            test_row = list(row)
            test_row[idx] = val
            score = get_score(header, test_row)
            if score < best_score:
                best_score = score
                recommendations[col_name] = val
                
    return recommendations

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]

        # Define levers based on problem context (Plan and Team Size)
        levers = {
            "Plan": (0.0, 1.0),
            "Team Size": (0.0, 1.0)
        }
        
        # Find a "bad" row (e.g., one with high cost and high idle)
        cost_idx = header.index("Cost-")
        idle_idx = header.index("Idle-")
        bad_row = max(rows, key=lambda r: r[cost_idx] + r[idle_idx])
        
        changes = fix(header, bad_row, levers)
        
        print("Customer Inquiry: Rescue Plan")
        print("Analysis: To reduce cost and idle time, we recommend the following adjustments:")
        for col, val in changes.items():
            print(f"  - Adjust '{col}' to {val:.4f}")
        print("\nThese changes are calculated to move the project toward a more optimal state.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
