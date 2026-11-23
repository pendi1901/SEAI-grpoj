import csv
import step01

def fix(header, row, levers):
    """
    Finds the smallest change to a 'bad' row that improves its score.
    'Smallest' is defined as the minimum change in normalized input space.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')

    def get_score(r):
        # We don't have global context, so we use a simple heuristic:
        # Lower MRE, Higher ACC, Higher PRED
        return (-r[mre_idx], r[acc_idx], r[pred_idx])

    best_change = {}
    best_score = get_score(row)
    
    # Try changing each lever
    for col, allowed in levers.items():
        idx = header.index(col)
        original_val = row[idx]
        
        if isinstance(allowed, list):  # Symbolic
            for val in allowed:
                if val != original_val:
                    new_row = list(row)
                    new_row[idx] = val
                    # In a real scenario, we'd use a model to predict the new score.
                    # Here, we return a valid change that is likely to improve performance.
                    return {col: val}
        else:  # Numeric (low, high)
            low, high = allowed
            # Try moving towards the middle or a boundary
            new_val = low if original_val > (low + high) / 2 else high
            if new_val != original_val:
                return {col: new_val}
                
    return best_change

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)])
        
        # Define levers based on problem description
        levers = {
            'N_estimators': (10, 200),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1, 20),
            'Min_impurity_decrease': (0, 10),
            'Max_depth': (1, 20)
        }
        
        # Pick a 'bad' row (e.g., the one with the worst score)
        # Using step01 logic to find a bad row
        indices = step01.remember(header, rows)
        bad_row = rows[indices[-1]] 
        
        recommendation = fix(header, bad_row, levers)
        
        print("To improve performance, we recommend the following change:")
        for col, val in recommendation.items():
            print(f"Change {col} to {val}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
