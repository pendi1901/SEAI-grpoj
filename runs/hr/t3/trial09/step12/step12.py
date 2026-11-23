import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the impact of cutting overtime on 'YearsAtCompany+' for Sales staff.
    We train a model on existing data and predict the outcome for test rows
    where 'overTime' is set to 'No' for all Sales employees.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    
    # Prepare features: exclude goal columns
    feature_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # Encode symbolic columns
    encoders = {}
    def encode_data(data_rows):
        processed = []
        for row in data_rows:
            new_row = []
            for i in feature_indices:
                val = row[i]
                if isinstance(val, str):
                    if i not in encoders:
                        # Fit on all training data
                        le = LabelEncoder()
                        le.fit([r[i] for r in train])
                        encoders[i] = le
                    new_row.append(encoders[i].transform([val])[0])
                else:
                    new_row.append(val)
            processed.append(new_row)
        return processed

    X_train = encode_data(train)
    y_train = [row[goal_idx] for row in train]
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Process test rows: force overTime to 'No' for Sales department
    modified_test = []
    for row in test:
        new_row = list(row)
        if new_row[dept_idx] == 'Sales':
            new_row[ot_idx] = 'No'
        modified_test.append(new_row)
        
    X_test = encode_data(modified_test)
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    # Scenario: Predict tenure for Sales staff if overtime is cut
    sales_rows = [r for r in rows if r[header.index('department')] == 'Sales']
    test_data = [list(r) for r in sales_rows[:10]]
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    for r in test_data: r[goal_idx] = "?"
    
    predictions = guess(header, rows, test_data)
    
    print("Impact Analysis: Cutting Overtime in Sales")
    print("Predicted average tenure (YearsAtCompany+) for Sales staff if overtime is removed:")
    print(f"{sum(predictions)/len(predictions):.2f} years")
    print("Logic: Model trained on historical data, simulating 'No' overtime for Sales.")
