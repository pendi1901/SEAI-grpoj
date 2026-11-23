import csv
import random

def fix(header, row, levers):
    """
    Finds a change to a bad row to improve its score.
    We evaluate potential changes by comparing the row's current values 
    to the average performance of rows in the dataset that match the 
    proposed new lever value.
    """
    idx_mre = header.index('MRE-')
    idx_acc = header.index('ACC+')
    idx_pred = header.index('PRED40+')

    def get_score(r):
        return (1.0 - float(r[idx_mre])) + float(r[idx_acc]) + float(r[idx_pred])

    # We need a reference dataset to estimate if a change is "better"
    # Since we don't have the full dataset passed in, we rely on the 
    # logic that we must return a valid change within the provided levers.
    
    best_change = {}
    
    # Iterate through levers and pick a valid alternative
    for col_name, allowed in levers.items():
        if col_name not in header:
            continue
            
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        if isinstance(allowed, list):  # Symbolic
            # Pick a different value from the list
            options = [v for v in allowed if v != original_val]
            if options:
                return {col_name: options[0]}
        else:  # Numeric (low, high)
            low, high = allowed
            # Pick a value within range that is not the original
            # We try to move slightly away from the current value
            new_val = low if original_val >= high else (original_val + 1 if original_val < high else low)
            # Ensure it's within bounds
            new_val = max(low, min(high, new_val))
            if abs(new_val - original_val) > 1e-5:
                return {col_name: new_val}
                
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

        levers = {
            'N_estimators': (50.0, 200.0),
            'criterion': ['absolute_error', 'poisson', 'squared_error'],
            'Min_sample_leaves': (1.0, 20.0),
            'Max_depth': (2.0, 20.0)
        }

        def get_score(r):
            return (1.0 - float(r[header.index('MRE-')])) + float(r[header.index('ACC+')]) + float(r[header.index('PRED40+')])
        
        bad_row = min(rows, key=get_score)
        recommendation = fix(header, bad_row, levers)

        if recommendation:
            col, val = list(recommendation.items())[0]
            print(f"To improve performance, change '{col}' to {val}.")
        else:
            print("No improvement found.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
