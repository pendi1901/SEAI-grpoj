import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column (YearsAtCompany+) for test rows
    based on input columns (non-goal columns).
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify goal columns
    goal_cols = [c for c in header if c.endswith('+') or c.endswith('-')]
    target_col = goal_cols[0]
    
    # Identify input columns (exclude goals)
    input_cols = [c for c in header if c not in goal_cols]
    
    # Preprocess: Encode symbolic columns
    combined = pd.concat([df_train[input_cols], df_test[input_cols]], axis=0)
    encoded_df = combined.copy()
    
    for col in input_cols:
        if encoded_df[col].dtype == 'object':
            le = LabelEncoder()
            encoded_df[col] = le.fit_transform(encoded_df[col].astype(str))
            
    X_train = encoded_df.iloc[:len(df_train)]
    X_test = encoded_df.iloc[len(df_train):]
    y_train = df_train[target_col].astype(float)
    
    # Train a simple regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    return predictions.tolist()

if __name__ == "__main__":
    # Load the data
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    # Split data for demonstration: use last 10 rows as 'test'
    train_data = rows[:-10]
    test_data = [row[:-3] + ["?", "?", "?"] for row in rows[-10:]]
    
    # Get estimates
    estimates = guess(header, train_data, test_data)
    
    print("Estimates for 'YearsAtCompany+' for new hires:")
    print("-" * 50)
    for i, est in enumerate(estimates):
        print(f"New Hire {i+1}: Predicted stay duration = {est:.2f} years")
    
    exit(0)
