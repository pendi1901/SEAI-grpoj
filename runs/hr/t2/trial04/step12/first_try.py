import csv
import step02

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    To answer the customer's question about cutting overtime in Sales,
    we simulate the effect by modifying the 'overTime' column in the test set
    to 'No' for all 'Sales' department employees, then using KNN to predict.
    """
    # Identify indices
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    
    # Prepare test data: simulate cutting overtime for Sales
    simulated_test = []
    for row in test:
        new_row = list(row)
        if new_row[dept_idx] == 'Sales':
            new_row[ot_idx] = 'No'
        simulated_test.append(new_row)
    
    # Use the existing KNN logic from step02 to estimate the goal
    return step02.guess(header, train, simulated_test)

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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split data
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Mask goals
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    # Get predictions
    predictions = guess(header, train_data, masked_test)
    
    # Calculate average impact for Sales employees
    dept_idx = header.index('department')
    sales_preds = [p for i, p in enumerate(predictions) if test_data[i][dept_idx] == 'Sales']
    
    if sales_preds:
        avg_stay = sum(sales_preds) / len(sales_preds)
        print("Analysis: If we cut overtime across Sales, the estimated average tenure (YearsAtCompany+) is:")
        print(f"{avg_stay:.2f} years.")
    else:
        print("No Sales employees found in the test set.")
