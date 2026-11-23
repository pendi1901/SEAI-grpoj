import csv
from step02 import guess
from step05 import blame

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics,
    excluding 'MonthlyIncome' or any pay-related levers.
    """
    # Load data to provide context for the regressor
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

    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    
    # Determine if we are maximizing or minimizing
    # We use the first goal column found
    g_idx = goal_indices[0]
    is_maximize = header[g_idx].endswith('+')
    
    best_change = {}
    best_val = -float('inf') if is_maximize else float('inf')
    
    # Iterate through allowed levers
    for col, options in levers.items():
        # Skip pay-related columns if they were in the levers
        if 'Income' in col or 'Salary' in col:
            continue
            
        col_idx = header.index(col)
        original_val = row[col_idx]
        
        candidates = []
        if isinstance(options, list):
            candidates = [o for o in options if o != original_val]
        else:
            # For numeric, try low, high, and midpoint
            candidates = [options[0], options[1], (options[0] + options[1]) / 2]
            
        for val in candidates:
            test_row = list(row)
            test_row[col_idx] = val
            
            # Predict impact
            pred = guess(header, rows, [test_row])[0]
            
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

    # Define non-monetary levers
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0),
        'WorkLifeBalance': (1.0, 4.0)
    }

    # Find a 'bad' row (e.g., low tenure)
    tenure_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda x: x[tenure_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Analysis: Since pay increases are not possible, we analyzed non-monetary levers.")
    print("Recommended changes to improve retention outcomes:")
    for col, val in recommendation.items():
        print(f" - Change '{col}' to {val}.")
