import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the value of the first goal column (YearsAtCompany+) 
    for test rows based on input features.
    """
    # Identify goal column (first column ending in + or -)
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    # Prepare training data
    # We use all columns except the goal columns as features
    feature_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # Encode symbolic columns
    encoders = {}
    def encode_data(data_rows, is_train=True):
        processed = []
        for row in data_rows:
            new_row = []
            for i in feature_indices:
                val = row[i]
                if isinstance(val, str):
                    if i not in encoders:
                        encoders[i] = LabelEncoder().fit([r[i] for r in train])
                    new_row.append(encoders[i].transform([val])[0])
                else:
                    new_row.append(val)
            processed.append(new_row)
        return processed

    X_train = encode_data(train)
    y_train = [row[goal_idx] for row in train]
    X_test = encode_data(test, is_train=False)
    
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
    
    # Split into train and a small test set for demonstration
    train_data = rows[:700]
    test_data = rows[700:710]
    
    # Mask the goal column for the test set
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    predictions = guess(header, train_data, masked_test)
    
    print("Estimates for 'YearsAtCompany+' (First 10 test rows):")
    for i, pred in enumerate(predictions):
        print(f"Row {i+1}: Predicted {pred:.2f} years")
