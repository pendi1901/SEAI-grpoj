import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the impact of cutting overtime on 'YearsAtCompany+' for Sales staff.
    We train a model on the training data and predict the goal for test rows
    where 'overTime' is set to 'No'.
    """
    # Identify the first goal column (ends with + or -)
    goal_cols = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_cols[0]
    
    # Prepare encoders for symbolic columns
    encoders = {}
    for i, col_name in enumerate(header):
        if i != target_idx and not header[i][0].isupper():
            encoders[i] = LabelEncoder()
            all_vals = [str(r[i]) for r in train]
            encoders[i].fit(all_vals)

    def transform_row(row, is_test=False):
        new_row = []
        for i, val in enumerate(row):
            if i == target_idx and is_test:
                new_row.append(0.0)
            elif i in encoders:
                try:
                    new_row.append(float(encoders[i].transform([str(val)])[0]))
                except ValueError:
                    new_row.append(0.0)
            else:
                new_row.append(float(val))
        return new_row

    # Prepare training features and target
    X_train = [transform_row(r) for r in train]
    y_train = [float(r[target_idx]) for r in train]
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict for test rows (simulating cutting overtime for Sales)
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    
    predictions = []
    for r in test:
        # Create a copy and simulate cutting overtime for Sales employees
        test_r = r[:]
        if test_r[dept_idx] == 'Sales':
            test_r[ot_idx] = 'No'
            
        X_test = transform_row(test_r, is_test=True)
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Focus on Sales department for the test set
    dept_idx = header.index('department')
    sales_rows = [r for r in rows if r[dept_idx] == 'Sales']
    
    # Use a subset for demonstration
    train_data = rows[:600]
    test_data = [r[:] for r in sales_rows[:10]]
    
    # Mask the goal column
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    for row in test_data:
        row[goal_idx] = "?"
        
    results = guess(header, train_data, test_data)
    
    print("Impact Analysis: Cutting Overtime in Sales")
    print("Predicted average tenure (YearsAtCompany+) if overtime is removed:")
    print(f"{sum(results) / len(results):.2f} years")
