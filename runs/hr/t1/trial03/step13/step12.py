import csv

def guess(header, train, test):
    """
    Estimates 'YearsAtCompany+' for test rows.
    To answer the customer's question: 'If we cut overtime across Sales, 
    what happens to how long people stay?', we model the relationship 
    between 'overTime', 'department', and 'YearsAtCompany+'.
    
    We use a conditional mean approach: for each test row, we estimate 
    the goal by calculating the average 'YearsAtCompany+' for training 
    rows that share the same 'department' and 'overTime' status.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    
    # Precompute averages for (department, overTime) groups
    groups = {}
    for row in train:
        key = (row[dept_idx], row[ot_idx])
        if key not in groups:
            groups[key] = []
        groups[key].append(row[goal_idx])
    
    group_means = {k: sum(v) / len(v) for k, v in groups.items()}
    global_mean = sum(row[goal_idx] for row in train) / len(train)
    
    predictions = []
    for t_row in test:
        # Simulate cutting overtime: if department is Sales, force overTime to 'No'
        dept = t_row[dept_idx]
        ot = 'No' if dept == 'Sales' else t_row[ot_idx]
        
        # Predict based on the group mean
        val = group_means.get((dept, ot), global_mean)
        predictions.append(float(val))
        
    return predictions

def load_data(filename):
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
    return header, rows

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    header, rows = load_data(filename)
    
    # Split data
    train = rows[:700]
    test = rows[700:]
    
    # Mask goal
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    masked_test = []
    for row in test:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    predictions = guess(header, train, masked_test)
    
    # Calculate impact for Sales
    sales_rows = [i for i, r in enumerate(test) if r[header.index('department')] == 'Sales']
    if sales_rows:
        avg_impact = sum(predictions[i] for i in sales_rows) / len(sales_rows)
        print(f"Analysis: Cutting overtime in Sales results in an estimated average tenure of {avg_impact:.2f} years.")
    else:
        print("No Sales employees found in the test set.")
    
    print("Strategy: We estimated tenure by grouping employees by department and overtime status, "
          "then applying the 'No Overtime' condition to the Sales department.")
