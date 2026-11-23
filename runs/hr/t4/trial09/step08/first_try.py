import csv
import random
import step02

def fix(header, row, levers):
    """
    Recommends a change for a 'bad' row (short tenure) to improve it.
    We simulate the impact of changing each lever by predicting the 
    'YearsAtCompany+' goal using the model from step02.
    """
    # Load historical data to train the model
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_data = next(reader)
        for r in reader:
            processed = []
            for i, val in enumerate(r):
                processed.append(float(val) if header_data[i][0].isupper() else val)
            rows.append(processed)

    # We need a model trained on the full dataset to predict outcomes
    # Since step02.guess takes (header, train, test), we use all rows as train
    # and the modified row as test.
    
    best_change = {}
    max_predicted_tenure = -1.0
    
    # Try each lever
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        # Determine test values to try
        test_values = []
        if isinstance(allowed, list): # Symbolic
            test_values = [v for v in allowed if v != original_val]
        else: # Numeric (low, high)
            test_values = [allowed[0], allowed[1], (allowed[0] + allowed[1]) / 2]
            
        for val in test_values:
            row_copy = row[:]
            row_copy[col_idx] = val
            
            # Predict tenure for this change
            prediction = step02.guess(header, rows, [row_copy])[0]
            
            if prediction > max_predicted_tenure:
                max_predicted_tenure = prediction
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)
            
    # Define levers as requested
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'PercentSalaryHike': (11, 25),
        'StockOptionLevel': (0, 3)
    }
    
    # Pick a "bad" row (e.g., low tenure)
    tenure_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda x: x[tenure_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Retention Improvement Analysis:")
    print(f"For an employee with low tenure ({bad_row[tenure_idx]} years),")
    for col, val in recommendation.items():
        print(f"we recommend changing '{col}' to '{val}'.")
    print("This change is predicted to improve long-term retention.")
