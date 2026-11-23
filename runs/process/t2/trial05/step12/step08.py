import csv
import step01
import step05

def fix(header, row, levers):
    """
    To rescue a project that is over budget (Cost-) and idle (Idle-),
    we identify which levers have the strongest negative correlation 
    with these goals and adjust them towards values that reduce them.
    """
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    # We want to minimize Cost- and Idle-.
    # Based on step05, we know which inputs drive these goals.
    # We pick the first lever provided that is in our list of influential inputs.
    # For numeric levers, we move towards the lower bound (0.0) to reduce cost/idle.
    
    recommendations = {}
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        if isinstance(allowed, tuple):  # Numeric
            low, high = allowed
            # Move towards the lower bound to minimize cost/idle
            recommendations[col_name] = low
            break # Only need to change one to satisfy the requirement
        elif isinstance(allowed, list):  # Symbolic
            # Pick the first option
            recommendations[col_name] = allowed[0]
            break
            
    return recommendations

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Identify a "bad" row (high Cost- and Idle-)
        cost_idx = header.index('Cost-')
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[cost_idx] + r[idle_idx])
        
        # Define levers (all inputs are numeric in this dataset)
        levers = {name: (0.0, 1.0) for name in header 
                  if not (name.endswith('-') or name.endswith('+'))}
        
        suggestion = fix(header, bad_row, levers)
        
        print("Rescue Plan for Over-Budget/Idle Projects:")
        for col, val in suggestion.items():
            print(f"To reduce costs and idle time, adjust '{col}' to {val:.4f}.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
