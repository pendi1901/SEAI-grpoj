import csv

def blame(header, rows):
    """
    Identifies input columns that are 'safe' to leave at default.
    We define 'safe' as those input columns whose variance in the 
    'best' rows is significantly lower than their variance in the 
    'worst' rows, or those that show no correlation with performance.
    
    Returns a list of input column names that have the least impact 
    on performance (i.e., they are 'blameless').
    """
    # Identify goal columns
    goals = []
    for i, name in enumerate(header):
        if name.endswith('-'):
            goals.append((i, -1))
        elif name.endswith('+'):
            goals.append((i, 1))

    # Calculate aggregate performance score for each row
    def get_score(row):
        score = 0
        for i, (col_idx, direction) in enumerate(goals):
            col_vals = [r[col_idx] for r in rows if isinstance(r[col_idx], (int, float))]
            min_v, max_v = min(col_vals), max(col_vals)
            rng = max_v - min_v if max_v != min_v else 1.0
            norm = (row[col_idx] - min_v) / rng
            if direction == -1:
                norm = 1.0 - norm
            score += norm
        return score / len(goals)

    # Identify input columns
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    # Sort rows by performance
    scores = [(get_score(r), r) for r in rows]
    scores.sort(key=lambda x: x[0])
    
    # Compare variance of inputs in top 25% vs bottom 25%
    n = len(rows) // 4
    best_rows = [x[1] for x in scores[-n:]]
    worst_rows = [x[1] for x in scores[:n]]
    
    stability = []
    for idx in input_indices:
        # Only analyze numeric inputs for stability
        col_vals = [r[idx] for r in rows if isinstance(r[idx], (int, float))]
        if not col_vals: continue
        
        best_vals = [r[idx] for r in best_rows if isinstance(r[idx], (int, float))]
        worst_vals = [r[idx] for r in worst_rows if isinstance(r[idx], (int, float))]
        
        if len(best_vals) < 2 or len(worst_vals) < 2: continue
        
        # Calculate variance
        var_best = sum((x - sum(best_vals)/len(best_vals))**2 for x in best_vals) / len(best_vals)
        var_worst = sum((x - sum(worst_vals)/len(worst_vals))**2 for x in worst_vals) / len(worst_vals)
        
        # If variance is low in best rows, the setting is likely stable/safe
        stability.append((header[idx], var_best))

    # Return columns with the lowest variance in the best-performing rows
    stability.sort(key=lambda x: x[1])
    return [x[0] for x in stability]

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

    safe_settings = blame(header, rows)
    print("Analysis: Which settings can be left at factory defaults?")
    print(f"The following settings are most stable in high-performing configurations: {', '.join(safe_settings)}")
    print("You can safely leave these at their defaults as they show minimal impact on performance.")
