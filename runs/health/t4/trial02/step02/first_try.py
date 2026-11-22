import csv
from step01 import remember
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor trained on the provided training data.
    """
    # Identify indices
    goal_idx = 0  # MRE-
    
    # Prepare training data
    # Convert symbolic columns to numeric for sklearn
    def encode_data(data):
        data_arr = np.array(data, dtype=object)
        # Identify symbolic columns (not numeric)
        # Based on prompt: Upper case = numeric, lower case = symbolic
        # criterion is the only symbolic column
        for i, col_name in enumerate(header):
            if col_name.islower():
                le = LabelEncoder()
                data_arr[:, i] = le.fit_transform(data_arr[:, i])
        return data_arr.astype(float)

    train_arr = encode_data(train)
    test_arr = encode_data(test)

    X_train = np.delete(train_arr, [0, 1, 2], axis=1) # Remove goals
    y_train = train_arr[:, goal_idx]
    
    X_test = np.delete(test_arr, [0, 1, 2], axis=1)

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
