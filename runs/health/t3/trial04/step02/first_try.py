import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor trained on the provided training data.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)

    # Identify goal columns and input columns
    goal_cols = [col for col in header if col.endswith('-') or col.endswith('+')]
    target_col = goal_cols[0]  # MRE-
    input_cols = [col for col in header if col not in goal_cols]

    # Prepare data
    X_train = df_train[input_cols].copy()
    y_train = df_train[target_col]
    X_test = df_test[input_cols].copy()

    # Encode symbolic columns
    for col in input_cols:
        if X_train[col].dtype == 'object':
            le = LabelEncoder()
            # Combine to ensure all categories are seen
            combined = pd.concat([X_train[col], X_test[col]], axis=0).astype(str)
            le.fit(combined)
            X_train[col] = le.transform(X_train[col].astype(str))
            X_test[col] = le.transform(X_test[col].astype(str))

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
                # Convert numeric columns, keep symbolic as strings
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split data for demonstration: 80% train, 20% test
    split_idx = int(len(rows) * 0.8)
    train_data = rows[:split_idx]
    test_data = rows[split_idx:]

    # Mask goals in test data
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    masked_test = []
    for row in test_data:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)

    predictions = guess(header, train_data, masked_test)
    
    print(f"Estimated MRE- for the first 5 test rows:")
    for i in range(min(5, len(predictions))):
        print(f"Row {i}: {predictions[i]:.4f}")
    print("...")
    print(f"Successfully generated {len(predictions)} forecasts.")
