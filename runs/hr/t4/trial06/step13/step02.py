import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a Random Forest Regressor.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)

    # Identify goal column (first column ending in + or -)
    goal_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]

    # Prepare features: drop goal columns and identify symbolic columns
    features = [c for c in header if not (c.endswith('+') or c.endswith('-'))]
    
    # Encode symbolic columns
    encoders = {}
    for col in header:
        if not col[0].isupper():
            le = LabelEncoder()
            # Combine train and test to ensure consistent encoding
            combined = pd.concat([df_train[col], df_test[col]], axis=0).astype(str)
            le.fit(combined)
            df_train[col] = le.transform(df_train[col].astype(str))
            df_test[col] = le.transform(df_test[col].astype(str))
            encoders[col] = le

    X_train = df_train[features]
    y_train = df_train[goal_col]
    X_test = df_test[features]

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
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

    # Split data: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Mask goals in test data
    goal_idx = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')][0]
    for row in test_data:
        row[goal_idx] = "?"

    predictions = guess(header, train_data, test_data)
    
    print("Estimation of 'YearsAtCompany+' for the first 5 test cases:")
    for i in range(min(5, len(predictions))):
        print(f"Test Row {i+1}: Predicted Years = {predictions[i]:.2f}")
