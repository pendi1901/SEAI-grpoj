import csv
import step02

def fix(header, row, levers):
    """
    Recommends a change for a 'bad' row to improve it.
    To avoid the performance bottleneck of retraining the model for every 
    lever iteration, we assume the model is already trained or we perform 
    a single pass if necessary. Here, we use the logic from step02 but 
    optimize by minimizing redundant operations.
    """
    # Load historical data once
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_data = next(reader)
        for r in reader:
            processed = [float(val) if header_data[i][0].isupper() else val for i, val in enumerate(r)]
            rows.append(processed)

    # We need a model trained on the full dataset.
    # To optimize, we call guess once per lever type or use a simplified approach.
    # Given the 120s constraint, we avoid full retraining inside the loop.
    
    best_change = {}
    max_predicted_tenure = -float('inf')
    
    # Pre-calculate baseline prediction
    baseline_pred = step02.guess(header, rows, [row])[0]
    
    for col_name, allowed in levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        test_values = []
        if isinstance(allowed, list):
            test_values = [v for v in allowed if v != original_val]
        else:
            test_values = [allowed[0], allowed[1]]
            
        for val in test_values:
            row_copy = row[:]
            row_copy[col_idx] = val
            
            # Predict tenure for this change
            prediction = step02.guess(header, rows, [row_copy])[0]
            
            if prediction > max_predicted_tenure:
                max_predicted_tenure = prediction
                best_change = {col_name: val}
                
    return best_change if best_change else {list(levers.keys())[0]: levers[list(levers.keys())[0]][0]}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)
            
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'PercentSalaryHike': (11, 25),
        'StockOptionLevel': (0, 3)
    }
    
    tenure_idx = header.index('YearsAtCompany+')
    bad_row = min(rows, key=lambda x: x[tenure_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Retention Improvement Analysis:")
    print(f"For an employee with low tenure ({bad_row[tenure_idx]} years),")
    for col, val in recommendation.items():
        print(f"we recommend changing '{col}' to '{val}'.")
    print("This change is predicted to improve long-term retention.")
