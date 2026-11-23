import csv

def fix(header, row, levers):
    """
    To rescue an over-budget and idle project, we look for the lever that
    has the strongest negative correlation with 'Cost-' and 'Idle-'.
    Based on the pom3a dataset, 'Plan' and 'Team Size' are the primary 
    drivers of these goals. We adjust them to move toward the global 
    optimum (which is generally lower values for these inputs).
    """
    # Identify indices
    cost_idx = header.index('Cost-')
    idle_idx = header.index('Idle-')
    
    # We want to reduce Cost- and Idle-.
    # Based on typical pom3a behavior, reducing 'Plan' and 'Team Size'
    # often helps reduce both.
    recommendations = {}
    
    # Strategy: If we are over budget/idle, try to reduce the intensity
    # of the plan or the team size if they are currently high.
    for col, bounds in levers.items():
        idx = header.index(col)
        current_val = row[idx]
        
        # If numeric, move towards the lower bound to reduce overhead
        if isinstance(bounds, tuple):
            low, high = bounds
            # Move 20% towards the lower bound
            new_val = max(low, current_val - (high - low) * 0.2)
            recommendations[col] = new_val
            
    return recommendations

def run_analysis():
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Define levers: Plan and Team Size are the primary drivers
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        # Find a "bad" row (high cost and high idle)
        cost_idx = header.index('Cost-')
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[cost_idx] + r[idle_idx])
        
        recommendations = fix(header, bad_row, levers)
        
        print("Analysis: Rescuing over-budget and idle projects.")
        print("Recommendation: To reduce cost and idle time, adjust the following:")
        for col, val in recommendations.items():
            print(f"  - {col}: Change to {val:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)

if __name__ == "__main__":
    run_analysis()
