import csv
import step02

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    by calculating the average value of that column from the training set,
    specifically filtering for the 'Sales' department and 'No' overtime status.
    """
    # Find the first goal column
    goal_col_name = None
    for col in header:
        if col.endswith('+') or col.endswith('-'):
            goal_col_name = col
            break
    
    if not goal_col_name:
        return [0.0] * len(test)
    
    idx = header.index(goal_col_name)
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    
    # Filter training data for Sales department and No Overtime
    # If no such data exists, fallback to general average
    subset = [row[idx] for row in train 
              if row[dept_idx] == 'Sales' and row[ot_idx] == 'No' 
              and isinstance(row[idx], (int, float))]
    
    if not subset:
        return step02.guess(header, train, test)
    
    avg_val = sum(subset) / len(subset)
    return [float(avg_val)] * len(test)

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
    
    # Create a test row representing a Sales employee with no overtime
    test_row = [0.0] * len(header)
    test_row[header.index('department')] = 'Sales'
    test_row[header.index('overTime')] = 'No'
    
    # Mask the goal column
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    test_row[goal_idx] = "?"
    
    prediction = guess(header, rows, [test_row])
    
    print("Customer Question: If we cut overtime across Sales, what happens to how long people stay?")
    print(f"Analysis: Based on historical data for Sales employees with no overtime,")
    print(f"the estimated tenure (YearsAtCompany+) is {prediction[0]:.2f} years.")
