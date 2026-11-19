import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) using a Random Forest Regressor.
    Handles symbolic columns by encoding them.
    """
    # Identify goal and input columns
    goal_idx = 0  # MRE-
    
    # Prepare data
    X_train = []
    y_train = []
    
    # Encode symbolic columns
    encoders = {}
    for i, col_name in enumerate(header):
        if isinstance(train[0][i], str):
            le = LabelEncoder()
            all_vals = [r[i] for r in train] + [r[i] for r in test]
            le.fit(all_vals)
            encoders[i] = le

    def transform_row(row):
        new_row = []
        for i, val in enumerate(row):
            if i in encoders:
                new_row.append(encoders[i].transform([val])[0])
            else:
                new_row.append(float(val))
        return new_row

    for row in train:
        y_train.append(row[goal_idx])
        X_train.append(transform_row(row)[1:]) # Exclude all goal columns
        
    X_test = [transform_row(row)[1:] for row in test]
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                # Convert numeric columns, keep symbolic as strings
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed.append(float(val))
                else:
                    processed.append(val)
            rows.append(processed)

    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask goals in test data
    masked_test = []
    for row in test_data:
        new_row = ["?" if i < 3 else val for i, val in enumerate(row)]
        masked_test.append(new_row)
        
    predictions = guess(header, train_data, masked_test)
    
    print("Forecast Analysis:")
    print(f"Estimated MRE- for the first 5 test configurations:")
    for i in range(min(5, len(predictions))):
        print(f"Row {700 + i}: {predictions[i]:.4f}")
