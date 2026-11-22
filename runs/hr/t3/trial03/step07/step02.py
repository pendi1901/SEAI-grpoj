import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the value of the first goal column ('YearsAtCompany+')
    for test rows using a Random Forest Regressor.
    """
    # Identify goal column (first column ending in '+' or '-')
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    # Prepare data
    # We use all columns except the goal column as features
    feature_indices = [i for i in range(len(header)) if i != goal_idx]
    
    # Encode symbolic columns
    encoders = {}
    def encode_data(data_rows):
        encoded = []
        for row in data_rows:
            new_row = []
            for i in feature_indices:
                val = row[i]
                if isinstance(val, str):
                    if i not in encoders:
                        encoders[i] = LabelEncoder().fit([r[i] for r in train])
                    try:
                        new_row.append(float(encoders[i].transform([val])[0]))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(float(val))
            encoded.append(new_row)
        return encoded

    X_train = encode_data(train)
    y_train = [row[goal_idx] for row in train]
    X_test = encode_data(test)
    
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
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Split data: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    for row in test_data:
        row[goal_idx] = "?"
        
    predictions = guess(header, train_data, test_data)
    
    print("Estimation of 'YearsAtCompany+' for the first 5 test cases:")
    for i in range(min(5, len(predictions))):
        print(f"Test Row {i}: Predicted Years = {predictions[i]:.2f}")
