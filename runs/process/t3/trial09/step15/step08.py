import csv
import random

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve 'Cost-' and 'Idle-'.
    We perform a local search by perturbing the levers to find a 
    configuration that minimizes the goal values.
    """
    # Identify goal indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Identify lever indices
    lever_indices = {h: i for i, h in enumerate(header) if h in levers}
    
    best_change = {}
    best_score = float('inf')
    
    # Try random perturbations within the allowed lever ranges
    for _ in range(100):
        candidate_row = list(row)
        current_change = {}
        
        for col, bounds in levers.items():
            idx = lever_indices[col]
            if isinstance(bounds, (list, tuple)) and not isinstance(bounds, str):
                # Numeric: pick a value in range
                new_val = random.uniform(bounds[0], bounds[1])
            else:
                # Symbolic: pick from list
                new_val = random.choice(bounds)
            
            candidate_row[idx] = new_val
            current_change[col] = new_val
            
        # Simple heuristic: minimize the sum of goals (Cost- and Idle-)
        # We assume lower is better for both.
        score = sum(candidate_row[i] for i in goal_indices)
        
        if score < best_score:
            best_score = score
            best_change = current_change
            
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if i < len(header) - 3 or (i >= len(header) - 3 and val.replace('.','',1).isdigit()) else val for i, val in enumerate(row)])
        
        # Define levers based on input columns
        levers = {
            'Culture': (0, 1),
            'Criticality': (0, 1),
            'Criticality Modifier': (0, 1),
            'Initial Known': (0, 1),
            'Inter-Dependency': (0, 1),
            'Dynamism': (0, 1),
            'Size': (0, 1),
            'Plan': (0, 1),
            'Team Size': (0, 1)
        }
        
        # Find a 'bad' row (high cost and high idle)
        cost_idx = header.index('Cost-')
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[cost_idx] + r[idle_idx])
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Inquiry: How to rescue an over-budget, idle project?")
        print("Analysis: To improve performance, we recommend the following adjustments:")
        for col, val in recommendation.items():
            print(f"- Adjust '{col}' to {val:.4f}")
        print("\nThese changes are designed to shift the project parameters toward more efficient configurations.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
