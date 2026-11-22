import csv
import numpy as np
from step02 import guess as original_guess

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor, with the 'N_estimators' halved.
    """
    n_est_idx = header.index('N_estimators')
    
    # Create a modified training set where N_estimators is halved
    modified_train = []
    for row in train:
        new_row = list(row)
        new_row[n_est_idx] = float(new_row[n_est_idx]) / 2.0
        modified_train.append(new_row)
        
    # Create a modified test set where N_estimators is halved
    # We must handle the '?' in the goal columns for the test set
    modified_test = []
    for row in test:
        new_row = list(row)
        new_row[n_est_idx] = float(new_row[n_est_idx]) / 2.0
        modified_test.append(new_row)
        
    # The original_guess function in step02.py fails when it encounters '?'
    # because it tries to convert it to float. We must provide a version 
    # that handles the '?' mask correctly.
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import LabelEncoder
    
    goal_idx = 0
    symbolic_cols = [i for i, name in enumerate(header) if name.islower()]
    all_data = modified_train + modified_test
    encoders = {}
    for col_idx in symbolic_cols:
        le = LabelEncoder()
        values = [row[col_idx] for row in all_data if row[col_idx] != '?']
        le.fit(values)
        encoders[col_idx] = le

    def prepare_features(data, is_train=True):
        processed = []
        for row in data:
            new_row = []
            for i, val in enumerate(row):
                if i in symbolic_cols:
                    new_row.append(encoders[i].transform([val])[0])
                elif val == '?':
                    new_row.append(0.0) # Placeholder for masked values
                else:
                    new_row.append(float(val))
            processed.append(new_row)
        return np.array(processed)

    train_arr = prepare_features(modified_train)
    X_train = train_arr[:, 3:]
    y_train = train_arr[:, goal_idx]
    
    test_arr = prepare_features(modified_test, is_train=False)
    X_test = test_arr[:, 3:]

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

    split = int(len(rows) * 0.8)
    train_data = rows[:split]
    test_data = rows[split:]
    masked_test = [['?'] * 3 + row[3:] for row in test_data]
    
    baseline_preds = original_guess(header, train_data, masked_test)
    avg_baseline = sum(baseline_preds) / len(baseline_preds)
    
    halved_preds = guess(header, train_data, masked_test)
    avg_halved = sum(halved_preds) / len(halved_preds)
    
    diff = avg_halved - avg_baseline
    print(f"Impact of halving the forecaster size (N_estimators):")
    print(f"Original average MRE: {avg_baseline:.4f}")
    print(f"Halved size average MRE: {avg_halved:.4f}")
    print(f"The forecast error (MRE) changes by {diff:.4f}.")
