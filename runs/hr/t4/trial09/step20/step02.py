import csv
import step01
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a Random Forest Regressor.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    target_idx = goal_indices[0]
    
    # Prepare data
    X_train = []
    y_train = []
    
    # Encode symbolic columns
    encoders = {}
    for i, name in enumerate(header):
        if not name[0].isupper():
            le = LabelEncoder()
            # Combine train and test to ensure all categories are seen
            # Filter out '?' from test for fitting
            all_vals = [row[i] for row in train] + [row[i] for row in test if row[i] != '?']
            le.fit(all_vals)
            encoders[i] = le

    def transform(row):
        new_row = []
        for i, val in enumerate(row):
            if i == target_idx: continue
            if i in encoders:
                # If test row has '?', replace with a neutral value (e.g., 0)
                val_to_transform = val if val != '?' else encoders[i].classes_[0]
                new_row.append(encoders[i].transform([val_to_transform])[0])
            else:
                # Handle '?' in numeric columns if any
                new_row.append(float(val) if val != '?' else 0.0)
        return new_row

    for row in train:
        X_train.append(transform(row))
        y_train.append(float(row[target_idx]))
        
    X_test = [transform(row) for row in test]
    
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
    
    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = [row[:] for row in rows[700:]]
    
    # Mask the goal column in test data
    goal_idx = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')][0]
    for row in test_data:
        row[goal_idx] = "?"
        
    predictions = guess(header, train_data, test_data)
    
    print("Estimation of 'YearsAtCompany+' for new hires:")
    print(f"{'Row':<10} | {'Predicted Years':<15}")
    print("-" * 30)
    for i, pred in enumerate(predictions[:5]):
        print(f"{i:<10} | {pred:.2f}")
    print("...")
