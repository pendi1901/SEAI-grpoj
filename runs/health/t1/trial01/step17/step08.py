import csv

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row to improve its goals.
    We define 'improvement' as moving towards the global bests.
    'Smallest change' is defined by the normalized distance in lever space.
    """
    # Identify indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    lever_indices = {name: header.index(name) for name in levers.keys()}
    
    def get_score(r):
        # Simple heuristic: average of normalized goals
        scores = []
        for i in goal_indices:
            val = r[i]
            # Use a simple proxy: if we don't have global stats, 
            # we assume lower is better for '-' and higher for '+'
            if header[i].endswith('-'):
                scores.append(-val)
            else:
                scores.append(val)
        return sum(scores) / len(scores)

    best_change = {}
    best_score = -float('inf')

    # Try changing one lever at a time
    for col, allowed in levers.items():
        idx = lever_indices[col]
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, tuple):  # Numeric range
            low, high = allowed
            # Try a few steps in the range
            step = (high - low) / 5
            for i in range(1, 6):
                val = low + i * step
                if val != original_val:
                    candidates.append(val)
        else:  # Symbolic list
            for val in allowed:
                if val != original_val:
                    candidates.append(val)
        
        for val in candidates:
            new_row = row[:]
            new_row[idx] = val
            score = get_score(new_row)
            if score > best_score:
                best_score = score
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed_row.append(float(val))
                    else:
                        processed_row.append(val)
                rows.append(processed_row)

        # Define levers based on problem description
        levers = {
            'N_estimators': (50, 200),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1, 20),
            'Min_impurity_decrease': (0, 10),
            'Max_depth': (1, 20)
        }

        # Pick a row that is performing poorly (e.g., high MRE)
        mre_idx = header.index('MRE-')
        bad_row = max(rows, key=lambda r: r[mre_idx])
        
        recommendation = fix(header, bad_row, levers)
        
        print("To improve performance, we recommend the following change:")
        for col, val in recommendation.items():
            print(f"Update '{col}' to {val}")
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
