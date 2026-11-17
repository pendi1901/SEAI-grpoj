import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Predicts the first goal column for test rows using a Random Forest Regressor.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify the target (first goal column)
    target_col = header[0]
    
    # Identify input columns (all columns except goals)
    # Goals end in '-' or '+'
    input_cols = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    
    # Prepare data
    X_train = df_train[input_cols].copy()
    y_train = df_train[target_col].astype(float)
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
    filename = 'Health-ClosedIssues0000.train.csv'
    data = []
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
            data.append(processed_row)
    
    # Split data for demonstration: use first 7000 as train, last 1000 as test
    train_data = data[:7000]
    test_data = [row[:] for row in data[7000:]]
    
    # Mask goals in test data
    for row in test_data:
        for i, col in enumerate(header):
            if col.endswith('-') or col.endswith('+'):
                row[i] = "?"
                
    predictions = guess(header, train_data, test_data)
    
    print("Forecast analysis complete.")
    print(f"Estimated value for the first goal column of the first test row: {predictions[0]:.4f}")
    print(f"Average predicted value across test set: {sum(predictions)/len(predictions):.4f}")
