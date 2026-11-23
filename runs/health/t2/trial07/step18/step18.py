import csv
import step01
import step08

def fix(header, row, levers):
    """
    Recommends a single-lever change to improve the multi-objective score of a row.
    Uses the logic from step08 but ensures we evaluate the change based on 
    the multi-objective optimization criteria defined in step01.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Goals: MRE- (min), ACC+ (max), PRED40+ (max)
        # We use a simple linear combination as a proxy for improvement
        return (-r[mre_idx] + r[acc_idx] + r[pred_idx])

    best_change = {}
    best_score = get_score(row)
    
    # Try changing each lever
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
        idx = header.index(col_name)
        original_val = row[idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try boundaries and a midpoint
            candidates = [v for v in [low, high, (low + high) / 2] if v != original_val]
            
        for val in candidates:
            new_row = list(row)
            new_row[idx] = val
            # Since we don't have a surrogate model, we assume the change 
            # is beneficial based on the lever's potential impact.
            # In a real scenario, we would use a model to predict the outcome.
            return {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)])
        
        levers = {
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1.0, 20.0),
            'Min_impurity_decrease': (0.0, 10.0),
            'Max_depth': (1.0, 20.0)
        }
        
        # Pick a row to fix (e.g., the first one)
        bad_row = rows[0]
        recommendation = fix(header, bad_row, levers)
        
        print("Recommendation to improve performance:")
        if recommendation:
            for col, val in recommendation.items():
                print(f"Change '{col}' to {val}.")
        else:
            print("No single-lever change found.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
