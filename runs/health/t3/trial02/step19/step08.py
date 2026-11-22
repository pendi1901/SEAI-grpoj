import csv

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row's settings that improves performance.
    We use a simple heuristic: evaluate the impact of changing each lever 
    by checking the average performance of rows in the dataset that match 
    the new lever value.
    """
    # Identify goal indices and directions
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))
        elif name.endswith('+'):
            goals.append((i, 1))

    def get_row_score(r):
        score = 0
        for i, direction in goals:
            val = r[i]
            score += (val * direction)
        return score

    # Find the best possible value for each lever based on historical data
    best_changes = {}
    
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        
        # Find all rows that have a specific value for this lever
        # and calculate their average performance
        candidates = []
        if isinstance(allowed, list):
            candidates = allowed
        else:
            # For numeric, sample a few points in the range
            low, high = allowed
            candidates = [low + (high - low) * i / 4 for i in range(5)]
            
        best_val = None
        max_avg_score = float('-inf')
        
        for val in candidates:
            # Filter rows that match this value (with tolerance for floats)
            if isinstance(val, float):
                matches = [r for r in rows if abs(r[idx] - val) < (high - low) * 0.1]
            else:
                matches = [r for r in rows if r[idx] == val]
            
            if matches:
                avg_score = sum(get_row_score(r) for r in matches) / len(matches)
                if avg_score > max_avg_score:
                    max_avg_score = avg_score
                    best_val = val
        
        if best_val is not None and best_val != row[idx]:
            best_changes[col_name] = best_val

    # Return the single best change found
    if best_changes:
        # Return the first recommended change
        k = list(best_changes.keys())[0]
        return {k: best_changes[k]}
    
    return {}

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    levers = {
        'N_estimators': (10.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    # Example usage on the first row
    recommendation = fix(header, rows[0], levers)
    
    print("Optimization Analysis:")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve performance, change '{col}' to {val}.")
    else:
        print("No simple single-lever change found to improve performance.")
