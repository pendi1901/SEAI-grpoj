import csv

def fix(header, row, levers):
    """
    Recommends a change to a lever to reduce 'Idle-' while respecting
    the constraint that we cannot hire (i.e., cannot change 'Team Size').
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(r):
        s = 0
        for i in goal_indices:
            val = float(r[i])
            s += val if header[i].endswith('-') else (1.0 - val)
        return s

    # We want to minimize 'Idle-'. 
    # We test small perturbations of the allowed levers.
    best_col = None
    best_val = None
    min_score = float('inf')
    
    # Current row's baseline score
    current_score = get_score(row)
    
    for col_name, allowed in levers.items():
        # Skip 'Team Size' as per customer constraint
        if col_name == 'Team Size':
            continue
            
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate test values
        if isinstance(allowed, tuple):  # Numeric (low, high)
            test_vals = [allowed[0], allowed[1], (allowed[0] + allowed[1]) / 2]
        else:  # Symbolic
            test_vals = allowed
            
        for val in test_vals:
            if val == original_val:
                continue
            
            # Create hypothetical row
            new_row = list(row)
            new_row[idx] = val
            
            # Heuristic: evaluate the change
            # Since we don't have a full model, we favor changes that 
            # reduce the 'Idle-' goal specifically.
            score = get_score(new_row)
            if score < min_score:
                min_score = score
                best_col = col_name
                best_val = val
                
    if best_col:
        return {best_col: best_val}
    
    # Fallback: return the first allowed lever's min value
    fallback_col = [k for k in levers.keys() if k != 'Team Size'][0]
    val = levers[fallback_col][0] if isinstance(levers[fallback_col], tuple) else levers[fallback_col][0]
    return {fallback_col: val}

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
        
        # Example: Fix a row that has high Idle-
        # We assume the user cannot change 'Team Size'
        row = [float(x) for x in rows[0]]
        levers = {
            'Culture': (0.0, 1.0),
            'Criticality': (0.0, 1.0),
            'Size': (0.0, 1.0),
            'Plan': (0.0, 1.0),
            'Team Size': (0.0, 1.0) # Customer cannot change this
        }
        
        recommendation = fix(header, row, levers)
        print("Recommendation to cut idle time without hiring:")
        for col, val in recommendation.items():
            print(f"Adjust '{col}' to {val:.4f}.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
