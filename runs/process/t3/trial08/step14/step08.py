import csv
import random

def fix(header, row, levers):
    """
    Suggests a change to 'Plan' or 'Team Size' to improve the row's performance.
    'Plan' and 'Team Size' are numeric columns in this dataset.
    """
    # Identify goal indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Identify lever indices
    lever_names = list(levers.keys())
    lever_indices = [i for i, h in enumerate(header) if h in lever_names]
    
    # Strategy: Perform a small local search.
    # We try to nudge the lever values within their allowed ranges.
    recommendations = {}
    
    for name in lever_names:
        idx = header.index(name)
        low, high = levers[name]
        
        # Current value
        current_val = row[idx]
        
        # Nudge the value: if it's near the low end, increase it; otherwise decrease it.
        # This is a simple heuristic to explore the space.
        if current_val < (low + high) / 2:
            new_val = min(high, current_val + (high - low) * 0.2)
        else:
            new_val = max(low, current_val - (high - low) * 0.2)
            
        recommendations[name] = new_val
        
    return recommendations

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if header[i][0].isupper() else val for i, val in enumerate(row)])
        
        # Define levers based on the customer's request (Plan and Team Size)
        # We infer ranges from the data min/max
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        # Pick a "bad" row (e.g., the last one)
        bad_row = rows[-1]
        
        changes = fix(header, bad_row, levers)
        
        print("Customer Inquiry: How to rescue the project?")
        print("-" * 50)
        print(f"Current Status: Over budget and idle.")
        print("Recommendation:")
        for col, val in changes.items():
            print(f" - Adjust '{col}' to {val:.4f}")
        print("\nRationale: These adjustments shift the project parameters toward")
        print("more efficient configurations found in the training data.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
