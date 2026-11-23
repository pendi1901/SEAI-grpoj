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

    # Identify goal columns
    goal_cols = [name for name in header if name.endswith('-') or name.endswith('+')]
    target_col = goal_cols[0]
    
    # Features are all columns except the goals
    features = [name for name in header if name not in goal_cols]
    
    # Encode symbolic columns
    encoders = {}
    for col in header:
        if df_train[col].dtype == 'object':
            le = LabelEncoder()
            # Combine train and test to ensure all categories are covered
            combined = pd.concat([df_train[col], df_test[col]], axis=0).astype(str)
            le.fit(combined)
            df_train[col] = le.transform(df_train[col].astype(str))
            df_test[col] = le.transform(df_test[col].astype(str))
            encoders[col] = le

    X_train = df_train[features]
    y_train = df_train[target_col]
    X_test = df_test[features]

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict
    predictions = model.predict(X_test)
    return predictions.tolist()

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for val in row:
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)

    # Split into train and a dummy test set (last 10 rows)
    train_data = rows[:-10]
    test_data = [row[:] for row in rows[-10:]]
    
    # Mask the goals in test data
    goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
    for row in test_data:
        for idx in goal_indices:
            row[idx] = "?"

    estimates = guess(header, train_data, test_data)
    
    print("Forecast estimation complete.")
    print(f"Estimated MRE- for the last 10 rows:")
    for i, val in enumerate(estimates):
        print(f"Row {i+1}: {val:.4f}")
