import csv
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row's settings that improves performance.
    'Smallest change' is defined by the number of levers adjusted.
    """
    def get_score(r):
        score = 0
        goals = [(i, h) for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for i, h in goals:
            val = r[i]
            if h.endswith('-'):
                score -= val
            else:
                score += val
        return score

    # Current performance
    current_score = get_score(row)
    best_change = {}
    best_score = current_score
    
    # Try changing one lever at a time
    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        # Generate candidates
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few steps within range
            step = (high - low) / 5
            for i in range(1, 6):
                val = low + i * step
                if abs(val - original_val) > 1e-6:
                    candidates.append(val)
        
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            new_score = get_score(new_row)
            if new_score > best_score:
                best_score = new_score
                best_change = {col_name: val}
                
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
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Define levers based on column types
    levers = {
        'N_estimators': (10, 200),
        'criterion': ['absolute_error', 'poisson', 'squared_error'],
        'Min_sample_leaves': (1, 20),
        'Min_impurity_decrease': (0, 10),
        'Max_depth': (1, 20)
    }

    # Pick a row that is likely 'bad' (e.g., first row)
    bad_row = rows[0]
    recommendation = fix(header, bad_row, levers)
    
    print("Optimization Analysis:")
    if recommendation:
        col, val = list(recommendation.items())[0]
        print(f"To improve performance, change '{col}' to {val}.")
    else:
        print("No simple single-lever change found to improve performance.")
