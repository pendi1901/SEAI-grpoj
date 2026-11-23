import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the impact of cutting overtime in Sales on 'YearsAtCompany+'.
    We train a model on the training data, then simulate the test set 
    with 'overTime' set to 'No' for all 'Sales' department employees.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    
    symbolic_indices = [i for i, name in enumerate(header) if not name[0].isupper()]
    
    # Fit encoders on all available data
    encoders = {}
    for i in symbolic_indices:
        encoders[i] = LabelEncoder()
        # Collect all possible values for symbolic columns
        all_vals = [row[i] for row in train] + [row[i] for row in test if row[i] != '?']
        encoders[i].fit(all_vals)
            
    def transform_row(row, is_test=False):
        new_row = []
        for i, val in enumerate(row):
            if i == goal_idx:
                continue
            if i in symbolic_indices:
                new_row.append(float(encoders[i].transform([val])[0]))
            else:
                # Handle '?' in test rows by using a neutral value (e.g., 0.0)
                if val == '?':
                    new_row.append(0.0)
                else:
                    new_row.append(float(val))
        return new_row

    X_train = [transform_row(row) for row in train]
    y_train = [float(row[goal_idx]) for row in train]
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = []
    for row in test:
        # Simulate cutting overtime for Sales
        simulated_row = row[:]
        if simulated_row[dept_idx] == 'Sales':
            simulated_row[ot_idx] = 'No'
            
        X_test = transform_row(simulated_row, is_test=True)
        predictions.append(float(model.predict([X_test])[0]))
        
    return predictions

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
                    try: processed_row.append(float(val))
                    except ValueError: processed_row.append(val)
                else: processed_row.append(val)
            rows.append(processed_row)
    
    # Use all data to train, then predict on the same data to see the effect
    train_data = rows
    test_data = [row[:] for row in rows]
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    for row in test_data:
        row[goal_idx] = '?'
        
    preds = guess(header, train_data, test_data)
    
    # Calculate average change for Sales employees
    dept_idx = header.index('department')
    sales_indices = [i for i, row in enumerate(rows) if row[dept_idx] == 'Sales']
    
    avg_orig = sum(rows[i][goal_idx] for i in sales_indices) / len(sales_indices)
    avg_new = sum(preds[i] for i in sales_indices) / len(sales_indices)
    
    print("Impact Analysis: Cutting Overtime in Sales")
    print(f"Average 'YearsAtCompany+' (Current): {avg_orig:.2f}")
    print(f"Average 'YearsAtCompany+' (If Overtime cut): {avg_new:.2f}")
    print("Conclusion: The model suggests that removing overtime in the Sales department "
          "would result in a shift in average tenure as shown above.")
