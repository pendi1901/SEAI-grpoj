import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def guess(header, train, test):
    """
    Estimates the value of the first goal column for each test row
    using K-Nearest Neighbors based on input features.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify input columns (those not ending in - or +)
    input_cols = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Identify the first goal column
    goal_cols = [col for col in header if col.endswith(('-', '+'))]
    target_col = goal_cols[0]
    
    # Prepare X and y
    X_train = df_train[input_cols]
    y_train = df_train[target_col]
    X_test = df_test[input_cols]
    
    # Use KNN to predict the target
    # n_neighbors=5 is a standard heuristic for small datasets
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    return predictions.tolist()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Split data: 80% train, 20% test
        split = int(len(rows) * 0.8)
        train_data = rows[:split]
        test_data = [row[:len(header)-3] + ['?'] * 3 for row in rows[split:]]
        
        predictions = guess(header, train_data, test_data)
        
        # Calculate average prediction to answer the customer
        avg_cost = sum(predictions) / len(predictions)
        
        print("Customer Inquiry Analysis:")
        print(f"Based on the provided data, the estimated cost for the requested setups")
        print(f"is approximately {avg_cost:.4f} units.")
        print("Note: This estimate is derived from a K-Nearest Neighbors model")
        print("trained on historical project performance data.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
