import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the value of the first goal column (YearsAtCompany+) 
    for test rows using a Random Forest Regressor.
    """
    # Identify goal column (first column ending in '+' or '-')
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    # Identify symbolic columns
    symbolic_indices = [i for i, name in enumerate(header) if not name[0].isupper()]
    
    # Fit encoders on all available data
    encoders = {}
    for i in symbolic_indices:
        encoders[i] = LabelEncoder()
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
                # If it's a test row and the value is '?', we shouldn't be using it 
                # as an input feature anyway, but here we ensure numeric conversion
                new_row.append(float(val))
        return new_row

    X_train = [transform_row(row) for row in train]
    y_train = [float(row[goal_idx]) for row in train]
    X_test = [transform_row(row) for row in test]
        
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict
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
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = [row[:] for row in rows[700:800]]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    for row in test_data:
        row[goal_idx] = '?'
        
    predictions = guess(header, train_data, test_data)
    
    print("Estimation of 'YearsAtCompany+' for the first 5 test cases:")
    for i in range(min(5, len(predictions))):
        print(f"Test Row {i}: Predicted {predictions[i]:.2f} years")
