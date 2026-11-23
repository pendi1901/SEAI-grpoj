import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Predicts the first goal column (MRE-) using a Random Forest Regressor.
    Handles symbolic columns by label encoding.
    """
    # Identify indices
    goal_idx = 0  # MRE-
    
    # Prepare data
    # We use all columns except the goals as features
    # Goals are columns ending in - or +
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    feature_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Encode symbolic columns
    encoders = {}
    def encode_data(data):
        encoded = []
        for row in data:
            new_row = []
            for i in feature_indices:
                val = row[i]
                if isinstance(val, str):
                    if i not in encoders:
                        encoders[i] = LabelEncoder().fit([r[i] for r in train])
                    new_row.append(encoders[i].transform([val])[0])
                else:
                    new_row.append(val)
            encoded.append(new_row)
        return encoded

    X_train = encode_data(train)
    y_train = [row[goal_idx] for row in train]
    X_test = encode_data(test)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict
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
                # Convert numeric columns to floats, keep symbolic as strings
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split into train and a dummy test set (last 10 rows) to demonstrate
    train_data = rows[:-10]
    test_data = [r[:] for r in rows[-10:]]
    
    # Mask goals in test data
    for row in test_data:
        for i in range(len(header)):
            if header[i].endswith('-') or header[i].endswith('+'):
                row[i] = "?"

    predictions = guess(header, train_data, test_data)
    
    print("Forecasts for the first 5 test rows (MRE-):")
    for i, pred in enumerate(predictions[:5]):
        print(f"Row {i+1}: {pred:.4f}")
    
    exit(0)
