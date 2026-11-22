import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a Random Forest Regressor, handling '?' in test data.
    """
    # Identify goal column (first column ending in + or -)
    goal_idx = -1
    for i, col in enumerate(header):
        if col.endswith('+') or col.endswith('-'):
            goal_idx = i
            break
    
    # Prepare data: encode symbolic columns using training data only
    # to ensure consistency and avoid '?' issues in test set
    encoders = {}
    
    def encode_row(row, is_train=True):
        encoded = []
        for i, val in enumerate(row):
            if i == goal_idx and not is_train:
                encoded.append(0.0)  # Placeholder for '?'
            elif isinstance(val, str):
                if i not in encoders:
                    le = LabelEncoder()
                    # Fit on all available string data from train
                    le.fit([r[i] for r in train])
                    encoders[i] = le
                encoded.append(float(encoders[i].transform([val])[0]))
            else:
                encoded.append(float(val))
        return encoded

    X_train = []
    y_train = []
    for row in train:
        encoded = encode_row(row, is_train=True)
        y_train.append(encoded[goal_idx])
        X_train.append(encoded[:goal_idx] + encoded[goal_idx+1:])
    
    X_test = []
    for row in test:
        encoded = encode_row(row, is_train=False)
        X_test.append(encoded[:goal_idx] + encoded[goal_idx+1:])
    
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
    
    # Split data: use last 100 as test
    train_data = rows[:-100]
    test_data = [r[:] for r in rows[-100:]]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+'))
    for row in test_data:
        row[goal_idx] = "?"
        
    predictions = guess(header, train_data, test_data)
    
    print(f"Estimated tenure for the first 5 test subjects:")
    for i in range(min(5, len(predictions))):
        print(f"Subject {i+1}: {predictions[i]:.2f} years")
