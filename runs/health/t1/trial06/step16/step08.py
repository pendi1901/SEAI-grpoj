import csv

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row to improve its performance.
    'Smallest change' is defined as the minimum Euclidean distance in 
    normalized input space.
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')
    
    def get_score(r):
        # Simple multi-objective score: minimize MRE, maximize ACC and PRED
        # We assume numeric values for goals
        return -r[idx_mre] + r[idx_acc] + r[idx_pred]

    best_change = {}
    min_dist = float('inf')

    for col_name, allowed in levers.items():
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, (list, tuple)) and not isinstance(allowed[0], (int, float)):
            # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:
            # Numeric (low, high)
            low, high = allowed
            # Try a small step or boundary values
            candidates = [low, high]
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            
            # Calculate distance (normalized)
            dist = 0
            if isinstance(val, (int, float)):
                dist = abs(val - original_val) / (high - low + 1e-9)
            else:
                dist = 1.0
                
            if dist < min_dist:
                min_dist = dist
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
                rows.append(processed)
        
        # Define levers based on dataset structure
        levers = {
            'N_estimators': (10, 200),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1, 20),
            'Min_impurity_decrease': (0, 10),
            'Max_depth': (1, 20)
        }
        
        # Pick a 'bad' row (e.g., the one with the lowest score)
        def score(r): return -r[0] + r[1] + r[2]
        bad_row = min(rows, key=score)
        
        recommendation = fix(header, bad_row, levers)
        
        print("To improve performance with the smallest change, we recommend:")
        for col, val in recommendation.items():
            print(f"Change '{col}' to {val}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
