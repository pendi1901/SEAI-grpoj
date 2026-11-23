import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a Random Forest Regressor after encoding symbolic columns.
    """
    # Identify goal column (first column ending in + or -)
    goal_col = next(c for c in header if c.endswith('+') or c.endswith('-'))
    
    # Prepare DataFrames
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Separate features and target
    X = df_train.drop(columns=[goal_col])
    y = df_train[goal_col]
    X_test = df_test.drop(columns=[goal_col])
    
    # Encode symbolic columns
    # We must ensure all columns are numeric for the regressor
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            # Combine train and test to ensure consistent encoding
            combined = pd.concat([X[col], X_test[col]], axis=0).astype(str)
            le.fit(combined)
            X[col] = le.transform(X[col].astype(str))
            X_test[col] = le.transform(X_test[col].astype(str))
        else:
            # Ensure numeric columns are float
            X[col] = X[col].astype(float)
            X_test[col] = X_test[col].astype(float)
            
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Predict
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    # Use the first 700 for training, last 100 for testing
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-'))
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = 0.0 # Placeholder value for the masked column
        masked_test.append(new_row)
    
    predictions = guess(header, train_data, masked_test)
    
    print("Estimation of 'YearsAtCompany+' for new hires:")
    print(f"{'Row Index':<10} | {'Predicted Years'}")
    print("-" * 30)
    for i, pred in enumerate(predictions[:5]):
        print(f"{i:<10} | {pred:.2f}")
    print("...")
