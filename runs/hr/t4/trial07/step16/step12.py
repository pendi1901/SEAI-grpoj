import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    We simulate the 'cut overtime' scenario by setting 'overTime' to 'No'
    for all test rows where the department is 'Sales', then predicting.
    """
    # Find the first goal column index
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            goal_idx = i
            break
            
    # Identify feature indices (all except goal)
    feature_indices = [i for i in range(len(header)) if i != goal_idx]
    
    # Apply the 'cut overtime' intervention to test data
    dept_idx = header.index('department')
    ot_idx = header.index('overTime')
    
    modified_test = []
    for row in test:
        new_row = list(row)
        if new_row[dept_idx] == 'Sales':
            new_row[ot_idx] = 'No'
        modified_test.append(new_row)

    # Encode data
    encoded_train = []
    encoded_test = []
    
    for i in feature_indices:
        col_train = [row[i] for row in train]
        col_test = [row[i] for row in modified_test]
        
        if not header[i][0].isupper():
            le = LabelEncoder()
            le.fit([str(x) for x in (col_train + col_test)])
            encoded_train.append(le.transform([str(x) for x in col_train]))
            encoded_test.append(le.transform([str(x) for x in col_test]))
        else:
            encoded_train.append([float(x) for x in col_train])
            encoded_test.append([float(x) for x in col_test])
                
    X_train = list(zip(*encoded_train))
    X_test = list(zip(*encoded_test))
    y_train = [row[goal_idx] for row in train]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model.predict(X_test).tolist()

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

    # Use first 700 to train, next 100 to simulate the intervention
    train_data = rows[:700]
    test_data = rows[700:800]
    
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            goal_idx = i
            break
            
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    predictions = guess(header, train_data, masked_test)
    
    avg_pred = sum(predictions) / len(predictions)
    print("Analysis: If we cut overtime in Sales, the predicted average tenure")
    print(f"('YearsAtCompany+') for the test group is {avg_pred:.2f} years.")
