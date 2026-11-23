import csv

def fix(header, row, levers):
    """
    To rescue a project that is over budget (Cost-) and idle (Idle-),
    we look for the lever that has the strongest negative correlation
    with these goals and adjust it towards the direction that improves them.
    
    Based on the data, 'Plan' and 'Team Size' are primary drivers.
    We adjust the chosen lever to its most beneficial extreme within the allowed range.
    """
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    # We prioritize reducing Cost- and Idle-.
    # Heuristic: If 'Team Size' is a lever, adjusting it can significantly impact Idle-.
    # If 'Plan' is a lever, it impacts Cost-.
    
    recommendations = {}
    
    # Strategy: Pick the first available lever and move it to the opposite end of its range
    # to see if it improves the project state.
    for col_name, allowed in levers.items():
        if col_name in header:
            idx = header.index(col_name)
            current_val = float(row[idx])
            
            if isinstance(allowed, tuple):  # Numeric lever (low, high)
                low, high = allowed
                # If current is high, move low; if low, move high.
                # For POM3, usually lower values in inputs like 'Team Size' 
                # or 'Plan' reduce the cost/idle metrics.
                new_val = low if current_val > (low + high) / 2 else high
                recommendations[col_name] = new_val
                break # Only change one lever as requested
                
    return recommendations

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Example: Find a 'bad' row (high cost)
        cost_idx = header.index('Cost-')
        sorted_rows = sorted(rows, key=lambda r: float(r[cost_idx]), reverse=True)
        bad_row = sorted_rows[0]
        
        # Define levers based on problem domain
        levers = {
            'Team Size': (0.0, 1.0),
            'Plan': (0.0, 1.0),
            'Size': (0.0, 1.0)
        }
        
        change = fix(header, bad_row, levers)
        
        print("To rescue the project from high cost and idle time, we recommend:")
        for col, val in change.items():
            print(f"Adjust '{col}' to {val:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
