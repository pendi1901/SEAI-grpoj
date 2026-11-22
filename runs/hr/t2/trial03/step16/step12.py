import csv
import step02

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    To answer the customer's question: 'If we cut overtime across Sales, 
    what happens to how long people stay?', we simulate the effect by 
    setting 'overTime' to 'No' for all Sales department rows in the test set,
    then using the KNN estimation logic from step02.
    """
    # Identify indices
    goal_col = [h for h in header if h.endswith('+') or h.endswith('-')][0]
    goal_idx = header.index(goal_col)
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    
    # Prepare test data: simulate cutting overtime for Sales
    simulated_test = []
    for t_row in test:
        new_row = list(t_row)
        if new_row[dept_idx] == 'Sales':
            new_row[ot_idx] = 'No'
        simulated_test.append(new_row)
        
    # Use the KNN logic from step02 to estimate the goal
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split data
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Mask goal
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+')][0]
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = 0.0
        masked_test.append(new_row)
        
    # Get estimates
    results = guess(header, train_data, masked_test)
    
    # Calculate average change for Sales employees
    dept_idx = header.index('department')
    sales_results = [results[i] for i, r in enumerate(test_data) if r[dept_idx] == 'Sales']
    
    if sales_results:
        avg_tenure = sum(sales_results) / len(sales_results)
        print("Analysis: Impact of cutting overtime in Sales on retention.")
        print(f"Estimated average tenure for Sales employees after cutting overtime: {avg_tenure:.2f} years.")
        print("Logic: Simulated 'overTime'='No' for all Sales roles and used KNN to project tenure.")
    else:
        print("No Sales employees found in the test set.")
