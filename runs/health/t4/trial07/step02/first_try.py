import csv
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np
import step01

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using K-Nearest Neighbors.
    """
    # Identify goal and input columns
    goal_idx = 0  # MRE-
    
    # Prepare training data
    X_train = []
    y_train = []
    
    # Encode symbolic columns
    encoders = {}
    for i, col in enumerate(header):
        if not col[0].isupper():
            encoders[i] = LabelEncoder()
            all_vals = [r[i] for r in train] + [r[i] for r in test]
            encoders[i].fit(all_vals)

    def transform_row(row):
        new_row = []
        for i, val in enumerate(row):
            if i == goal_idx: continue
            if i in encoders:
                new_row.append(encoders[i].transform([val])[0])
            else:
                new_row.append(float(val))
        return new_row

    for row in train:
        X_train.append(transform_row(row))
        y_train.append(row[goal_idx])
        
    # Prepare test data
    X_test = [transform_row(row) for row in test]
    
    # Use KNN to predict the MRE- value
    model = KNeighborsRegressor(n_neighbors=5)
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
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split into train and a dummy test set (last 5 rows) to demonstrate
    train_data = rows[:-5]
    test_data = [r[:] for r in rows[-5:]]
    for r in test_data:
        r[0] = "?" # Mask the goal
        
    predictions = guess(header, train_data, test_data)
    
    print("Forecast analysis complete.")
    print("Estimated MRE- values for the last 5 rows:")
    for i, val in enumerate(predictions):
        print(f"Row {len(train_data) + i}: {val:.4f}")
