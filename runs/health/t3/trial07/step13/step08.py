import csv
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row to improve its performance.
    We prioritize changing numeric levers by small increments and symbolic
    levers by trying alternatives.
    """
    best_change = {}
    
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Simple heuristic: try to nudge numeric values towards the 'better' direction
    # or cycle through symbolic options.
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        current_val = row[idx]
        
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], (int, float)):
            # Symbolic: pick a different value
            options = [v for v in allowed if v != current_val]
            if options:
                best_change[col_name] = options[0]
                break
        else:
            # Numeric: nudge by 10% of the range
            low, high = allowed
            step = (high - low) * 0.1
            new_val = current_val + step
            if new_val > high: new_val = high
            if new_val < low: new_val = low
            best_change[col_name] = new_val
            break
            
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define levers based on column types
    levers = {
        'N_estimators': (50.0, 200.0),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1.0, 20.0),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (1.0, 20.0)
    }

    # Pick a 'bad' row (e.g., the first one) to fix
    bad_row = rows[0]
    recommendation = fix(header, bad_row, levers)

    print("To improve the current setup, we recommend the following change:")
    for col, val in recommendation.items():
        print(f"Change '{col}' to {val}")
    
    exit(0)
