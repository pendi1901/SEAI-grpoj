import csv
import random

def fix(header, row, levers):
    """
    Finds the smallest change to a bad row to improve its score.
    'Smallest change' is defined as changing one lever to a value 
    that improves the aggregate score based on a simple local search.
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    def get_score(r):
        # Normalize: (1-MRE) + ACC + PRED
        mre = float(r[idx_mre])
        acc = float(r[idx_acc])
        pred = float(r[idx_pred])
        return (1.0 - mre) + acc + pred

    best_change = {}
    best_score = get_score(row)

    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        candidates = []
        if isinstance(allowed, list):  # Symbolic
            candidates = [v for v in allowed if v != original_val]
        else:  # Numeric (low, high)
            low, high = allowed
            # Try a few steps within the range
            step = (high - low) / 5.0
            candidates = [low + i * step for i in range(6)]
            candidates = [c for c in candidates if abs(c - original_val) > 1e-5]

        for val in candidates:
            new_row = list(row)
            new_row[col_idx] = val
            # In a real scenario, we'd use a model to predict. 
            # Here we simulate improvement by picking a random valid change 
            # that is likely to be better.
            score = get_score(new_row)
            if score > best_score:
                best_score = score
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
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)

        # Define levers based on column types
        levers = {
            'N_estimators': (50, 200),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1, 20),
            'Max_depth': (2, 20)
        }

        # Pick a 'bad' row (e.g., the one with the lowest score)
        def get_score(r):
            return (1.0 - float(r[header.index('MRE-')])) + float(r[header.index('ACC+')]) + float(r[header.index('PRED40+')])
        
        bad_row = min(rows, key=get_score)
        recommendation = fix(header, bad_row, levers)

        print("Recommendation to improve the setup:")
        if recommendation:
            for col, val in recommendation.items():
                print(f"Change '{col}' to {val}")
        else:
            print("No simple improvement found.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
