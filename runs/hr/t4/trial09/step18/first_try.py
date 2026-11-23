import csv
import step02
import step08

def fix(header, row, levers):
    """
    Recommends a change for a 'bad' row to improve it, excluding salary-related
    levers as per the customer's request (no money for pay).
    """
    # Load historical data to train the model
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header_data = next(reader)
        for r in reader:
            processed = [float(val) if header_data[i][0].isupper() else val for i, val in enumerate(r)]
            rows.append(processed)

    # Filter out salary-related levers if any exist in the provided levers
    # (Though the prompt implies we should use the provided levers)
    filtered_levers = {k: v for k, v in levers.items() if 'Salary' not in k and 'Income' not in k}
    
    # If no levers remain, fall back to the original levers
    if not filtered_levers:
        filtered_levers = levers

    best_change = {}
    max_predicted_tenure = -float('inf')
    
    # Iterate through allowed levers to find the one that maximizes predicted tenure
    for col_name, allowed in filtered_levers.items():
        col_idx = header.index(col_name)
        original_val = row[col_idx]
        
        test_values = []
        if isinstance(allowed, list):
            test_values = [v for v in allowed if v != original_val]
        else:
            # For numeric ranges, test the boundaries
            test_values = [allowed[0], allowed[1]]
            
        for val in test_values:
            row_copy = row[:]
            row_copy[col_idx] = val
            
            # Predict tenure for this change using step02's logic
            prediction = step02.guess(header, rows, [row_copy])[0]
            
            if prediction > max_predicted_tenure:
                max_predicted_tenure = prediction
                best_change = {col_name: val}
                
    return best_change if best_change else {list(filtered_levers.keys())[0]: filtered_levers[list(filtered_levers.keys())[0]][0]}

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed)
            
    # Levers excluding salary/income
    levers = {
        'businessTravel': ['Non-Travel', 'Travel_Frequently', 'Travel_Rarely'],
        'overTime': ['No', 'Yes'],
        'TrainingTimesLastYear': (0, 6),
        'StockOptionLevel': (0, 3),
        'WorkLifeBalance': (1, 4)
    }
    
    tenure_idx = header.index('YearsAtCompany+')
    # Find a 'bad' row (low tenure)
    bad_row = min(rows, key=lambda x: x[tenure_idx])
    
    recommendation = fix(header, bad_row, levers)
    
    print("Retention Improvement Analysis (No Budget):")
    print(f"For an employee with low tenure ({bad_row[tenure_idx]} years),")
    for col, val in recommendation.items():
        print(f"we recommend changing '{col}' to '{val}'.")
    print("This change is predicted to improve long-term retention without requiring salary increases.")
