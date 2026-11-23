import csv

def fix(header, row, levers):
    """
    Recommends changes to levers to minimize 'Idle-'.
    We find the best-performing rows in the dataset and suggest moving
    the current row's levers towards the values found in those top rows.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    idle_idx = header.index('Idle-')
    
    def get_score(r):
        # Lower is better for Idle-
        return float(r[idle_idx])

    # Load all data to find the "best" configurations
    filename = 'pom3a.n1000.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_file = next(reader)
        rows = [r for r in reader]

    # Find the top 10% of rows based on Idle-
    scored = sorted([(get_score(r), r) for r in rows], key=lambda x: x[0])
    best_rows = [r for s, r in scored[:max(1, len(rows) // 10)]]

    recommendations = {}
    for col_name, bounds in levers.items():
        col_idx = header.index(col_name)
        
        # Calculate the average value of this lever in the best rows
        best_vals = [float(r[col_idx]) for r in best_rows]
        target_val = sum(best_vals) / len(best_vals)
        
        # Clamp target to allowed bounds
        low, high = bounds
        new_val = max(low, min(high, target_val))
        
        recommendations[col_name] = new_val
        
    return recommendations

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
        
        # Find a "bad" row (high Idle-)
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: float(r[idle_idx]))
        
        # Levers excluding 'Team Size' (since hiring is not allowed)
        # We assume all other numeric inputs are adjustable levers
        levers = {
            'Culture': (0.0, 1.0),
            'Criticality': (0.0, 1.0),
            'Criticality Modifier': (0.0, 1.0),
            'Initial Known': (0.0, 1.0),
            'Inter-Dependency': (0.0, 1.0),
            'Dynamism': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Plan': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Inquiry: How to cut idle time without hiring?")
        print("-" * 60)
        print("Analysis: To reduce idle time, we recommend adjusting the following:")
        for col, val in recommendation.items():
            print(f"  {col} -> {val:.4f}")
        print("\nThese adjustments align your project parameters with top-performing setups.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
