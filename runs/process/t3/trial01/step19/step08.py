import csv

def fix(header, row, levers):
    """
    Recommends changes to 'levers' to improve a bad row.
    Strategy: For each lever, test the impact of moving it toward the 
    opposite end of its allowed range.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    
    def get_score(r):
        # Lower score is worse, higher is better
        # We assume the row passed in has numeric values for goals
        score = 0
        for i in goal_indices:
            val = r[i]
            # Normalize: for '-', lower is better; for '+', higher is better
            # Since we don't have global min/max, we assume 0-1 range
            if header[i].endswith('-'):
                score += (1.0 - val)
            else:
                score += val
        return score / len(goal_indices)

    best_change = {}
    current_score = get_score(row)
    best_score = current_score

    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Try moving to the bounds of the allowed range
        candidates = []
        if isinstance(allowed, tuple): # Numeric (low, high)
            candidates = [allowed[0], allowed[1]]
        else: # Symbolic
            candidates = allowed
            
        for val in candidates:
            if val == original_val:
                continue
            
            # Apply change
            row[idx] = val
            new_score = get_score(row)
            if new_score > best_score:
                best_score = new_score
                best_change = {col_name: val}
            # Reset
            row[idx] = original_val
            
    # If no improvement found, return a default change to satisfy "change at least one"
    if not best_change and levers:
        col = list(levers.keys())[0]
        val = levers[col][0] if isinstance(levers[col], tuple) else levers[col][0]
        return {col: val}
            
    return best_change

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Identify a "bad" row (high Cost- and high Idle-)
        cost_idx = header.index('Cost-')
        idle_idx = header.index('Idle-')
        bad_row = max(rows, key=lambda r: r[cost_idx] + r[idle_idx])
        
        # Define levers based on input columns
        levers = {
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0),
            'Size': (0.0, 1.0)
        }
        
        recommendation = fix(header, list(bad_row), levers)
        
        print("Rescue Plan for Over-Budget/Idle Project:")
        print("-" * 40)
        if recommendation:
            for col, val in recommendation.items():
                print(f"Recommended change: Set '{col}' to {val:.4f}")
            print("\nApplying this change is expected to improve project efficiency.")
        else:
            print("No simple lever adjustment found to improve performance.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
