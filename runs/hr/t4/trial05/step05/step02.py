import csv
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a K-Nearest Neighbors regressor.
    """
    # Identify goal column (first one ending in + or -)
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    # Prepare data: convert symbolic to numeric
    def encode_rows(data):
        encoded = []
        for row in data:
            new_row = []
            for i, val in enumerate(row):
                if isinstance(val, str):
                    # Simple label encoding for symbolic columns
                    new_row.append(float(hash(val) % 1000))
                else:
                    new_row.append(float(val))
            encoded.append(new_row)
        return encoded

    train_encoded = encode_rows(train)
    test_encoded = encode_rows(test)
    
    # Features: all columns except the goal
    X_train = [r[:goal_idx] + r[goal_idx+1:] for r in train_encoded]
    y_train = [r[goal_idx] for r in train_encoded]
    X_test = [r[:goal_idx] + r[goal_idx+1:] for r in test_encoded]
    
    # Train model
    model = KNeighborsRegressor(n_neighbors=5)
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
    
    # Split for demonstration: use last 10 rows as test
    train_data = rows[:-10]
    test_data = [r[:] for r in rows[-10:]]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    for row in test_data:
        row[goal_idx] = "?"
        
    predictions = guess(header, train_data, test_data)
    
    print("Estimated tenure for the last 10 employees:")
    for i, pred in enumerate(predictions):
        print(f"Employee {i+1}: {pred:.2f} years")
