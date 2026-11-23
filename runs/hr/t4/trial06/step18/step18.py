import csv
import random
import step02

def fix(header, row, levers):
    """
    Recommends changes to a 'bad' row to improve its goal metrics.
    To avoid long execution times, we use a single-pass evaluation of 
    levers rather than re-training models inside the loop.
    """
    goal_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]
    is_maximize = goal_col.endswith('+')
    
    # Load data once to train a single model
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_file = next(reader)
        for r in reader:
            processed_row = [float(val) if header_file[i][0].isupper() else val for i, val in enumerate(r)]
            rows.append(processed_row)

    # Train model once
    train_data = rows
    
    best_change = {}
    best_val = -float('inf') if is_maximize else float('inf')
    
    # Evaluate each lever
    for col, allowed in levers.items():
        idx = header.index(col)
        
        # Test a few representative values
        options = []
        if isinstance(allowed, list):
            options = allowed
        else:
            options = [allowed[0], (allowed[0] + allowed[1]) / 2, allowed[1]]
            
        for test_val in options:
            test_row = list(row)
            test_row[idx] = test_val
            
            # Predict
            prediction = step02.guess(header, train_data, [test_row])[0]
            
            if (is_maximize and prediction > best_val) or (not is_maximize and prediction < best_val):
                best_val = prediction
                best_change = {col: test_val}
                
    return best_change

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)

    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0.0, 6.0),
        'StockOptionLevel': (0.0, 3.0),
        'EnvironmentSatisfaction': (1.0, 4.0)
    }

    years_idx = header.index('YearsAtCompany+')
    bad_rows = [r for r in rows if r[years_idx] < 2.0]
    
    if bad_rows:
        sample_row = bad_rows[0]
        recommendations = fix(header, sample_row, levers)
        
        print("Analysis: Non-monetary retention strategies.")
        print(f"For an employee with {sample_row[years_idx]} years at the company, we suggest:")
        for col, val in recommendations.items():
            print(f"- Change '{col}' to: {val}")
    else:
        print("No 'bad' rows found to analyze.")
