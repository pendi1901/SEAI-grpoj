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
    
    # Prepare training data
    X_train = []
    y_train = []
    
    # Label encode symbolic columns
    encoders = {}
    for i, name in enumerate(header):
        if not name[0].isupper():
            encoders[i] = LabelEncoder()
            # Combine train and test to fit encoder
            all_vals = [row[i] for row in train] + [row[i] for row in test if row[i] != '?']
            encoders[i].fit(all_vals)
            
    def transform_row(row):
        new_row = []
        for i, val in enumerate(row):
            if i == goal_idx:
                continue
            if i in encoders:
                new_row.append(encoders[i].transform([val])[0])
            else:
                new_row.append(float(val))
        return new_row

    for row in train:
        X_train.append(transform_row(row))
        y_train.append(float(row[goal_idx]))
        
    # Prepare test data
    X_test = []
    for row in test:
        X_test.append(transform_row(row))
        
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
    test_data = rows[700:800]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    for row in test_data:
        row[goal_idx] = '?'
        
    predictions = guess(header, train_data, test_data)
    
    print("Estimation of 'YearsAtCompany+' for the first 5 test cases:")
    for i in range(min(5, len(predictions))):
        print(f"Test Row {i}: Predicted {predictions[i]:.2f} years")
