import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a Random Forest Regressor.
    """
    # Identify goal column (first column ending in '+' or '-')
    goal_idx = -1
    for i, col in enumerate(header):
        if col.endswith('+') or col.endswith('-'):
            goal_idx = i
            break
    
    # Prepare data: convert symbolic columns to numeric for scikit-learn
    def encode_data(data):
        encoded = []
        encoders = {}
        for i in range(len(header)):
            if isinstance(data[0][i], str):
                le = LabelEncoder()
                col_data = [row[i] for row in data]
                le.fit(col_data)
                encoders[i] = le
                encoded.append(le.transform(col_data))
            else:
                encoded.append([row[i] for row in data])
        return list(zip(*encoded)), encoders

    # Encode training data
    X_train_raw = [row[:goal_idx] + row[goal_idx+1:] for row in train]
    y_train = [row[goal_idx] for row in train]
    
    X_train, encoders = encode_data(X_train_raw)
    
    # Encode test data using same encoders
    X_test_raw = [row[:goal_idx] + row[goal_idx+1:] for row in test]
    X_test = []
    for row in X_test_raw:
        new_row = []
        for i, val in enumerate(row):
            if i in encoders:
                # Handle potential unseen labels by mapping to 0
                try:
                    new_row.append(encoders[i].transform([val])[0])
                except ValueError:
                    new_row.append(0)
            else:
                new_row.append(val)
        X_test.append(new_row)
        
    # Train model
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
    
    # Split: use first 700 for train, next 100 for test
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Mask goals in test data
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    for row in test_data:
        row[goal_idx] = "?"
        
    predictions = guess(header, train_data, test_data)
    
    print("Estimates for 'YearsAtCompany+' (first 5 test rows):")
    for i in range(min(5, len(predictions))):
        print(f"Row {i+700}: {predictions[i]:.2f} years")
