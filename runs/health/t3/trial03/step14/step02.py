import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor. Symbolic columns are label-encoded.
    """
    # Identify goal column (first one) and input columns
    goal_idx = 0
    
    # Prepare data
    def process_data(data):
        X = []
        y = []
        for row in data:
            # Inputs are all columns except the goals
            # Goals are columns ending in '-' or '+'
            inputs = []
            for i, val in enumerate(row):
                if not (header[i].endswith('-') or header[i].endswith('+')):
                    inputs.append(val)
            X.append(inputs)
            if len(row) > goal_idx and isinstance(row[goal_idx], (int, float)):
                y.append(row[goal_idx])
        return X, y

    # Encode symbolic columns
    # Identify which columns are symbolic (not numeric)
    symbolic_cols = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+')) and isinstance(train[0][i], str)]
    
    # Combine train and test for consistent encoding
    all_data = train + test
    encoders = {}
    for col_idx in symbolic_cols:
        le = LabelEncoder()
        col_values = [row[col_idx] for row in all_data]
        le.fit(col_values)
        encoders[col_idx] = le
        
    def transform(data):
        transformed = []
        for row in data:
            new_row = []
            for i, val in enumerate(row):
                if not (header[i].endswith('-') or header[i].endswith('+')):
                    if i in encoders:
                        new_row.append(encoders[i].transform([val])[0])
                    else:
                        new_row.append(val)
            transformed.append(new_row)
        return transformed

    X_train, y_train = transform(train), [row[goal_idx] for row in train]
    X_test = transform(test)
    
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
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split for demonstration: use last 100 as test
    train_data = rows[:-100]
    test_data = [[val if not (header[i].endswith('-') or header[i].endswith('+')) else "?" 
                  for i, val in enumerate(row)] for row in rows[-100:]]
    
    predictions = guess(header, train_data, test_data)
    
    print("Forecast Analysis:")
    print(f"Estimated MRE- for the last 5 test configurations:")
    for i in range(5):
        print(f"Row {len(rows)-100+i}: {predictions[i]:.4f}")
