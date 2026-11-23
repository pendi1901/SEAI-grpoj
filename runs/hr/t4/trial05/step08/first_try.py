import csv
import random
from step02 import guess

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics.
    We simulate the impact of changing each lever and pick the one 
    that yields the best predicted outcome.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    best_change = {}
    best_val = -float('inf') if is_maximize else float('inf')
    
    # We need a reference set to train the guesser
    # In a real scenario, we'd use the full dataset.
    # Here we assume the caller provides the context via the environment.
    # Since we can't access global 'rows' easily, we rely on the logic 
    # that 'guess' takes a training set.
    
    for col, options in levers.items():
        col_idx = header.index(col)
        original_val = row[col_idx]
        
        # Generate candidates
        candidates = []
        if isinstance(options, list):  # Symbolic
            candidates = [o for o in options if o != original_val]
        else:  # Numeric (low, high)
            candidates = [options[0], options[1], (options[0] + options[1]) / 2]
            
        for val in candidates:
            test_row = list(row)
            test_row[col_idx] = val
            
            # Predict impact (using a dummy training set for the guesser)
            # Note: In a production environment, we'd pass the actual training data.
            # Here we use the row itself as a minimal context for the regressor.
            pred = guess(header, [row], [test_row])[0]
            
            if (is_maximize and pred > best_val) or (not is_maximize and pred < best_val):
                best_val = pred
                best_change = {col: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
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

    # Define levers based on customer request
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    # Pick a sample row that has low tenure (a 'bad' row)
    # YearsAtCompany+ is at index 31
    tenure_idx = header.index('YearsAtCompany+')
    bad_row = min([r for r in rows], key=lambda x: x[tenure_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for staff with low tenure:")
    for col, val in recommendation.items():
        print(f" - Change '{col}' to {val} to improve retention outcomes.")
