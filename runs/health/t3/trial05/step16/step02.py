import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

def guess(header, train, test):
    """
    Predicts the first goal column (MRE-) for test rows using a Random Forest.
    Handles '?' in test rows by skipping them during transformation.
    """
    goal_idx = 0  # MRE-
    
    # Identify symbolic columns
    symbolic_indices = [i for i, val in enumerate(train[0]) if isinstance(val, str)]
    
    # Encode symbolic columns
    encoders = {}
    for i in symbolic_indices:
        le = LabelEncoder()
        all_vals = [r[i] for r in train] + [r[i] for r in test if r[i] != "?"]
        le.fit(all_vals)
        encoders[i] = le

    def transform_row(row, is_test=False):
        new_row = []
        for i, val in enumerate(row):
            if i == goal_idx and is_test:
                continue
            if i in symbolic_indices:
                new_row.append(encoders[i].transform([val])[0])
            else:
                # If it's a numeric column that is '?', we treat as 0 or handle appropriately
                # In this dataset, only goal columns are '?' in test
                new_row.append(float(val))
        return new_row

    X_train = [transform_row(row) for row in train]
    y_train = [row[goal_idx] for row in train]
    
    # Remove goal column from X_train
    X_train = [row[1:] for row in X_train]
    
    X_test = []
    for row in test:
        # Transform row, skipping the goal column index
        transformed = []
        for i, val in enumerate(row):
            if i == goal_idx:
                continue
            if i in symbolic_indices:
                transformed.append(encoders[i].transform([val])[0])
            else:
                transformed.append(float(val))
        X_test.append(transformed)

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
        
        # Split data: 80% train, 20% test
        split = int(len(rows) * 0.8)
        train_data = rows[:split]
        test_data = [r[:] for r in rows[split:]]
        for r in test_data:
            r[0] = "?"
        
        predictions = guess(header, train_data, test_data)
        
        print("Forecast analysis complete.")
        print(f"Estimated MRE for the first 5 test cases: {[round(p, 4) for p in predictions[:5]]}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
