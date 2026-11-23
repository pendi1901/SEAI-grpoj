import csv
import random
from step02 import guess

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics.
    We simulate the impact of changing each lever and pick the one 
    that yields the best predicted outcome.
    """
    # Load the full dataset to provide context for the regressor
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_file = next(reader)
        for r in reader:
            processed_row = []
            for i, val in enumerate(r):
                if header_file[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    best_change = {}
    best_val = -float('inf') if is_maximize else float('inf')
    
    # Use the full dataset to train the guesser so n_neighbors <= n_samples_fit
    train_data = rows
    
    for col, options in levers.items():
        col_idx = header.index(col)
        original_val = row[col_idx]
        
        candidates = []
        if isinstance(options, list):
            candidates = [o for o in options if o != original_val]
        else:
            candidates = [options[0], options[1], (options[0] + options[1]) / 2]
            
        for val in candidates:
            test_row = list(row)
            test_row[col_idx] = val
            
            # Predict impact using the full dataset for training
            pred = guess(header, train_data, [test_row])[0]
            
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

    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'PercentSalaryHike': (11.0, 25.0),
        'StockOptionLevel': (0.0, 3.0)
    }

    tenure_idx = header.index('YearsAtCompany+')
    bad_row = min([r for r in rows], key=lambda x: x[tenure_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Recommended changes for staff with low tenure:")
    for col, val in recommendation.items():
        print(f" - Change '{col}' to {val} to improve retention outcomes.")
