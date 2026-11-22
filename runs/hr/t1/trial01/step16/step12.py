import csv

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    To answer the customer's question about cutting overtime in Sales,
    we calculate the average tenure for Sales employees who do NOT work overtime
    and use that as our estimate for any test rows that are in Sales.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    first_goal_idx = goal_indices[0]
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    
    # Calculate baseline for Sales employees who do not work overtime
    sales_no_ot = [
        row[first_goal_idx] for row in train 
        if row[dept_idx] == 'Sales' and row[ot_idx] == 'No'
    ]
    
    # Fallback to global average if no specific data exists
    if sales_no_ot:
        baseline = sum(sales_no_ot) / len(sales_no_ot)
    else:
        baseline = sum(row[first_goal_idx] for row in train) / len(train)
        
    return [float(baseline) for _ in test]

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
            
    # Simulate a test scenario: Sales employees currently working overtime
    # We want to estimate their tenure if they were to stop working overtime.
    test_rows = [row for row in rows if row[header.index('department')] == 'Sales' and row[header.index('overTime')] == 'Yes']
    train_rows = [row for row in rows if row not in test_rows]
    
    # Mask goal columns in test
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    for row in test_rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    predictions = guess(header, train_rows, test_rows)
    
    if predictions:
        avg_pred = sum(predictions) / len(predictions)
        print("Analysis: Impact of cutting overtime in Sales on tenure (YearsAtCompany+).")
        print(f"Estimated average tenure for Sales staff after eliminating overtime: {avg_pred:.2f} years.")
        print("Conclusion: Based on current non-overtime Sales staff, this is the projected tenure outcome.")
    else:
        print("Insufficient data to estimate impact.")
