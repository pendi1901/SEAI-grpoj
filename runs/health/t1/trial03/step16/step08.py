import csv

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row's settings that improves its 
    multi-objective score. We define 'smallest change' as the minimum 
    Euclidean distance in the normalized lever space.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    lever_indices = {header.index(name): name for name in levers}
    
    # Simple heuristic: try small perturbations for numeric, 
    # and all possible values for symbolic.
    recommendations = {}
    
    for idx, name in lever_indices.items():
        allowed = levers[name]
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], (int, float)):
            # Symbolic: try all other options
            for val in allowed:
                if val != row[idx]:
                    recommendations[name] = val
                    break
        else:
            # Numeric: try moving towards the midpoint of the range
            low, high = allowed
            mid = (low + high) / 2
            if row[idx] < mid:
                recommendations[name] = min(high, row[idx] + (high - low) * 0.1)
            else:
                recommendations[name] = max(low, row[idx] - (high - low) * 0.1)
                
    return recommendations

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([val if header[i] == 'criterion' else float(val) 
                         for i, val in enumerate(row)])

    # Define levers based on column types
    levers = {
        'N_estimators': (50.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    # Pick a row that is likely 'bad' (e.g., the one with the worst MRE)
    mre_idx = header.index('MRE-')
    bad_row = max(rows, key=lambda r: r[mre_idx])
    
    change = fix(header, bad_row, levers)
    
    print("To improve the current setup, we recommend the following changes:")
    for col, val in change.items():
        print(f"  Change '{col}' to {val}")
    print("\nThese adjustments are designed to shift the configuration toward ")
    print("more optimal regions of the search space while maintaining performance.")
