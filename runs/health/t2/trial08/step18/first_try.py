import csv
from step01 import remember

def fix(header, row, levers):
    """
    Finds the single lever change that maximizes the row's performance score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # Score = (1 - MRE) + ACC + PRED (higher is better)
        return (1.0 - r[mre_idx]) + r[acc_idx] + r[pred_idx]

    best_change = {}
    best_score = get_score(row)
    
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
            # Test boundaries and midpoint
            for val in [float(low), float((low + high) / 2.0), float(high)]:
                if val != original_val:
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
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
                rows.append(processed)
        
        levers = {
            'N_estimators': (10.0, 200.0),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1.0, 20.0),
            'Min_impurity_decrease': (0.0, 10.0),
            'Max_depth': (1.0, 20.0)
        }
        
        # Find a 'bad' row (not in top 5%)
        best_indices = remember(header, rows)
        bad_row = next((r for i, r in enumerate(rows) if i not in best_indices), None)
        
        if bad_row:
            recommendation = fix(header, bad_row, levers)
            if recommendation:
                col, val = list(recommendation.items())[0]
                print(f"To improve your setup, change '{col}' to {val}.")
            else:
                print("No single lever change found to improve performance.")
        else:
            print("No bad rows found to improve.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
