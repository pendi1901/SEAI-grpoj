import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor trained on the provided training data.
    """
    # Identify goal and input columns
    goal_idx = 0  # MRE-
    
    # Prepare training data
    X_train = []
    y_train = []
    
    # Encode symbolic columns (criterion)
    # We need to handle the 'criterion' column which is at index 4
    le = LabelEncoder()
    
    # Combine train and test to ensure consistent encoding
    all_data = train + test
    criterion_col = [row[4] for row in all_data]
    le.fit(criterion_col)
    
    def transform_row(row):
        # Numeric columns: 0, 1, 2, 3, 5, 6, 7
        # Symbolic: 4
        new_row = [float(row[i]) if i != 4 else float(le.transform([row[i]])[0]) 
                   for i in range(len(row)) if i != goal_idx]
        return new_row

    X_train = [transform_row(row) for row in train]
    y_train = [row[goal_idx] for row in train]
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict test rows
    X_test = [transform_row(row) for row in test]
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
                # Convert numeric columns to floats, keep symbolic as strings
                if header[i] not in ['criterion']:
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Split into train and a dummy test set (last 10 rows)
    train_data = rows[:-10]
    test_data = [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]] for r in rows[-10:]]
    # Mask the goals in test data
    for r in test_data:
        r[0] = "?"
        r[1] = "?"
        r[2] = "?"
        
    estimates = guess(header, train_data, test_data)
    
    print("Forecast estimation complete.")
    print(f"Estimated MRE- for the last 10 configurations:")
    for i, est in enumerate(estimates):
        print(f"Row {i+1}: {est:.4f}")
