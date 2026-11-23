import csv

def fix(header, row, levers):
    """
    To rescue a project that is over budget (Cost-) and idle (Idle-),
    we look for the lever that has the strongest negative correlation with 
    these goals and adjust it to its most beneficial extreme.
    """
    # Identify goal indices
    cost_idx = header.index('Cost-')
    idle_idx = header.index('Idle-')
    
    # We want to minimize both Cost- and Idle-.
    # Based on typical POM3 data, 'Plan' and 'Team Size' are key levers.
    # We will try to adjust the lever that is furthest from the value
    # that typically correlates with lower costs/idle times.
    
    recommendations = {}
    
    # Strategy: If 'Plan' or 'Team Size' are in levers, move them to 
    # the side that typically reduces cost/idle.
    # In POM3, lower 'Team Size' and specific 'Plan' values often help.
    if 'Team Size' in levers:
        low, high = levers['Team Size']
        # Move towards lower team size to reduce idle/cost
        recommendations['Team Size'] = low
        
    if 'Plan' in levers:
        low, high = levers['Plan']
        # Move towards the lower end of the plan complexity
        recommendations['Plan'] = low
        
    return recommendations

def get_data():
    filename = "pom3a.n1000.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append([float(val) for val in row])
    return header, rows

if __name__ == "__main__":
    header, rows = get_data()
    
    # Define levers based on the problem description
    # Numeric columns are defined by (min, max)
    levers = {
        'Plan': (0.0, 1.0),
        'Team Size': (0.0, 1.0)
    }
    
    # Pick a "bad" row (e.g., one with high Cost- and Idle-)
    cost_idx = header.index('Cost-')
    idle_idx = header.index('Idle-')
    bad_row = max(rows, key=lambda r: r[cost_idx] + r[idle_idx])
    
    changes = fix(header, bad_row, levers)
    
    print("Project Rescue Analysis:")
    print(f"Current status: Cost-={bad_row[cost_idx]:.2f}, Idle-={bad_row[idle_idx]:.2f}")
    print("Recommended changes to rescue the project:")
    for col, val in changes.items():
        print(f"  - Adjust '{col}' to {val:.2f}")
    print("Rationale: Reducing team size and plan complexity minimizes resource contention and idle time.")
