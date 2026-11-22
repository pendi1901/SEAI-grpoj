import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor. Handles symbolic encoding and masked test data.
    """
    # Identify indices
    goal_idx = 0
    
    # Identify symbolic columns
    symbolic_cols = [i for i, name in enumerate(header) if name.islower()]
    
    # Combine train and test to ensure consistent label encoding
    all_data = train + test
    encoders = {}
    for col_idx in symbolic_cols:
        le = LabelEncoder()
        # Collect all unique values from train and test (ignoring '?')
        values = [row[col_idx] for row in all_data if row[col_idx] != '?']
        le.fit(values)
        encoders[col_idx] = le

    def prepare_features(data):
        processed = []
        for row in data:
            new_row = []
            for i, val in enumerate(row):
                if i in symbolic_cols:
                    new_row.append(encoders[i].transform([val])[0])
                else:
                    new_row.append(float(val))
            processed.append(new_row)
        return np.array(processed)

    # Prepare training data (X: inputs, y: goal)
    # Inputs are columns 3 to end
    train_arr = prepare_features(train)
    X_train = train_arr[:, 3:]
    y_train = train_arr[:, goal_idx]
    
    # Prepare test data (X: inputs)
    test_arr = prepare_features(test)
    X_test = test_arr[:, 3:]

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
                if header[i].isupper() or header[i] in ['N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split data: use 80% for training, 20% for testing
    split = int(len(rows) * 0.8)
    train_data = rows[:split]
    test_data = rows[split:]
    
    # Mask goals in test data
    masked_test = []
    for row in test_data:
        masked_row = ['?'] * 3 + row[3:]
        masked_test.append(masked_row)
        
    predictions = guess(header, train_data, masked_test)
    
    avg_mre = sum(predictions) / len(predictions)
    print(f"Estimated average MRE for new setups: {avg_mre:.4f}")
