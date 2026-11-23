import csv

def fix(header, row, levers):
    """
    Finds the best change to 'Plan' and 'Team Size' to minimize 'Cost-' and 'Idle-'.
    We perform a local search by testing small perturbations within the allowed levers.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        score = 0.0
        for i in goal_indices:
            val = r[i]
            if header[i].endswith('-'):
                score += val
            else:
                score += (1.0 - val)
        return score

    best_change = {}
    best_score = get_score(row)
    
    # Try small adjustments for each lever
    for col_name, bounds in levers.items():
        idx = header.index(col_name)
        low, high = bounds
        
        # Test a few points in the range
        for step in [0.1, 0.25, 0.5]:
            # Try moving towards the lower bound
            new_val = max(low, row[idx] - step)
            if new_val != row[idx]:
                temp_row = list(row)
                temp_row[idx] = new_val
                s = get_score(temp_row)
                if s < best_score:
                    best_score = s
                    best_change = {col_name: new_val}
            
            # Try moving towards the upper bound
            new_val = min(high, row[idx] + step)
            if new_val != row[idx]:
                temp_row = list(row)
                temp_row[idx] = new_val
                s = get_score(temp_row)
                if s < best_score:
                    best_score = s
                    best_change = {col_name: new_val}
                    
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Identify a "bad" row (high cost and high idle)
        cost_idx = header.index('Cost-')
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[cost_idx] + r[idle_idx])
        
        # Define levers based on the customer's request (Plan and Team Size)
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Inquiry: Rescue Plan for Over-Budget/Idle Projects")
        print("-" * 60)
        if recommendation:
            for col, val in recommendation.items():
                print(f"Recommendation: Adjust '{col}' to {val:.4f}")
            print("\nApplying this change will optimize resource allocation and reduce idle time.")
        else:
            print("No significant improvement found with current levers.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
