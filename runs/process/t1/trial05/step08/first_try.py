import csv

def fix(header, row, levers):
    """
    Finds the smallest change to 'Plan' or 'Team Size' to improve 'Cost-' and 'Idle-'.
    We perform a local search by perturbing the levers and picking the one that
    results in the best improvement to the goal scores.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        total = 0
        for i in goal_indices:
            val = float(r[i])
            if header[i].endswith('-'):
                total += val
            else:
                total += (1.0 - val)
        return total

    best_change = {}
    best_score = get_score(row)
    
    # Try small perturbations for numeric levers
    for col_name, bounds in levers.items():
        col_idx = header.index(col_name)
        original_val = float(row[col_idx])
        low, high = bounds
        
        # Try moving towards the center or boundaries to see if score improves
        # We test a few steps in the allowed range
        for step in [-0.1, 0.1]:
            new_val = max(low, min(high, original_val + step))
            if new_val == original_val:
                continue
                
            # Create a candidate row
            candidate = list(row)
            candidate[col_idx] = new_val
            
            # Simple heuristic: if score improves, this is a candidate
            # In a real scenario, we'd use a model, but here we assume 
            # the row's own goals are the target to minimize
            score = get_score(candidate)
            if score < best_score:
                best_score = score
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
        
        # Define levers
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0)
        }
        
        recommendation = fix(header, bad_row, levers)
        
        print("Customer Inquiry: How to rescue an over-budget, idle program?")
        print("-" * 60)
        if recommendation:
            print("Recommendation: Adjust the following parameters:")
            for col, val in recommendation.items():
                print(f"  {col} -> {val:.4f}")
        else:
            print("No simple adjustment found to improve performance.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
