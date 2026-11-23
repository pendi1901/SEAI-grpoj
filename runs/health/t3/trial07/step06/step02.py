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
    goals = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    target_col = header[goals[0]]
    
    # Prepare features: drop all goal columns
    feature_cols = [name for name in header if not (name.endswith('-') or name.endswith('+'))]
    
    # Encode symbolic columns
    encoders = {}
    for col in header:
        if isinstance(df_train[col].iloc[0], str):
            le = LabelEncoder()
            # Combine train and test to ensure consistent encoding
            combined = pd.concat([df_train[col], df_test[col]])
            le.fit(combined)
            df_train[col] = le.transform(df_train[col])
            df_test[col] = le.transform(df_test[col])
            encoders[col] = le
            
    X_train = df_train[feature_cols]
    y_train = df_train[target_col]
    X_test = df_test[feature_cols]
    
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
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Split: use first 700 for train, last 100 for test
    train_data = rows[:700]
    test_data = [row[:] for row in rows[700:]]
    
    # Mask goals in test data
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for row in test_data:
        for idx in goal_indices:
            row[idx] = "?"
            
    estimates = guess(header, train_data, test_data)
    
    print(f"Estimated MRE- for the first 5 test cases:")
    for i in range(min(5, len(estimates))):
        print(f"Row {700 + i}: {estimates[i]:.4f}")
