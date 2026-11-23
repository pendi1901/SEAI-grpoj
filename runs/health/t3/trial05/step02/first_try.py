import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

def guess(header, train, test):
    """
    Predicts the first goal column (MRE-) for test rows using a Random Forest.
    """
    # Identify goal and input columns
    goal_idx = 0  # MRE-
    
    # Prepare training data
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
        X_train.append(transform_row(row)[:goal_idx] + transform_row(row)[goal_idx+1:])

    # Prepare test data
    X_test = []
    for row in test:
        # Replace "?" with 0 for processing, though we don't use the goal column
        processed = transform_row(row)
        X_test.append(processed[:goal_idx] + processed[goal_idx+1:])

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Split data: 80% train, 20% test for demonstration
        split = int(len(rows) * 0.8)
        train_data = rows[:split]
        test_data = [[r[0] if i != 0 else "?" for i, r_val in enumerate(r)] for r in rows[split:]]
        
        predictions = guess(header, train_data, test_data)
        
        print("Forecast analysis complete.")
        print(f"Estimated MRE for the first 5 test cases: {[round(p, 4) for p in predictions[:5]]}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
