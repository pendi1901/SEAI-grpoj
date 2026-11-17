import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a Random Forest Regressor.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify the target column (first column ending in + or -)
    # Based on the prompt, 'YearsAtCompany+' is the first goal column.
    target_col = [c for c in header if c.endswith('+') or c.endswith('-')][0]
    
    # Prepare data: Encode symbolic columns
    df_all = pd.concat([df_train, df_test], axis=0)
    
    le_map = {}
    for col in df_all.columns:
        if df_all[col].dtype == 'object':
            le = LabelEncoder()
            # Convert to string to handle potential mixed types
            df_all[col] = le.fit_transform(df_all[col].astype(str))
            le_map[col] = le
            
    # Split back
    train_encoded = df_all.iloc[:len(df_train)]
    test_encoded = df_all.iloc[len(df_train):]
    
    X_train = train_encoded.drop(columns=[target_col])
    y_train = train_encoded[target_col].astype(float)
    X_test = test_encoded.drop(columns=[target_col])
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict
    predictions = model.predict(X_test)
    return predictions.tolist()

if __name__ == "__main__":
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    header = df.columns.tolist()
    rows = df.values.tolist()
    
    # Split data: use first 1000 for training, next 10 for testing
    train_data = rows[:1000]
    test_data = rows[1000:1010]
    
    # Mask the goal column in test data
    target_idx = header.index('YearsAtCompany+')
    for row in test_data:
        row[target_idx] = "?"
        
    results = guess(header, train_data, test_data)
    
    print("Estimates for 'YearsAtCompany+' for the first 10 test cases:")
    for i, val in enumerate(results):
        print(f"Test Row {i+1}: Predicted {val:.2f} years")
