import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor trained on the provided training data.
    """
    # Identify goal columns and input columns
    goal_idx = 0  # MRE- is the first column
    
    # Prepare training data
    # Convert symbolic columns to numeric for sklearn
    def preprocess(data):
        processed = []
        for row in data:
            new_row = []
            for i, val in enumerate(row):
                if isinstance(val, str):
                    # Simple label encoding for symbolic columns
                    new_row.append(hash(val) % 1000)
                else:
                    new_row.append(float(val))
            processed.append(new_row)
        return np.array(processed)

    train_data = preprocess(train)
    test_data = preprocess(test)

    # Split into X (inputs) and y (first goal)
    # Input columns are those not ending in - or +
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    X_train = train_data[:, input_indices]
    y_train = train_data[:, goal_idx]
    X_test = test_data[:, input_indices]

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)
    return predictions.tolist()

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

    # Split into train and a small test set for demonstration
    split = int(len(rows) * 0.8)
    train_set = rows[:split]
    test_set = []
    for r in rows[split:]:
        # Mask the goals with "?"
        new_r = [("?" if (header[i].endswith('-') or header[i].endswith('+')) else val) 
                 for i, val in enumerate(r)]
        test_set.append(new_r)

    estimates = guess(header, train_set, test_set)
    
    print("Forecast analysis complete.")
    print(f"Estimated MRE- for the first 5 test cases: {[round(x, 4) for x in estimates[:5]]}")
