import csv
from step02 import guess as base_guess

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    To answer the customer's question, we simulate the impact of cutting 
    overtime for the 'Sales' department.
    """
    # Identify indices
    overtime_idx = header.index('overTime')
    dept_idx = header.index('department')
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    
    # Create a modified test set where Sales overtime is set to 'No'
    # We must ensure the goal column is a placeholder that the base_guess 
    # logic can handle (it expects '?' to be ignored or handled).
    modified_test = []
    for row in test:
        new_row = list(row)
        if new_row[dept_idx] == 'Sales':
            new_row[overtime_idx] = 'No'
        # Ensure the goal column is '?' as expected by the harness/base_guess
        new_row[goal_idx] = '?'
        modified_test.append(new_row)
        
    return base_guess(header, train, modified_test)

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

    # Prepare data
    train_data = rows
    test_data = [list(row) for row in rows]
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    for row in test_data:
        row[goal_idx] = "?"

    # Get predictions
    predictions = guess(header, train_data, test_data)
    
    # Calculate average tenure for Sales employees
    dept_idx = header.index('department')
    sales_tenures = [predictions[i] for i in range(len(test_data)) if rows[i][dept_idx] == 'Sales']
    
    if sales_tenures:
        avg_tenure = sum(sales_tenures) / len(sales_tenures)
        print("Analysis: Impact of cutting overtime in Sales on tenure (YearsAtCompany+).")
        print(f"Projected average tenure for Sales staff after cutting overtime: {avg_tenure:.2f} years.")
    else:
        print("No Sales employees found in the dataset.")
