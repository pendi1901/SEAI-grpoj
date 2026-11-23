import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor

def guess(header, train, test):
    """
    Estimates the first goal column for test rows using K-Nearest Neighbors.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify input columns (those not ending in - or +)
    inputs = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    
    # Identify the first goal column
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    target = goals[0]
    
    # Prepare data
    X_train = df_train[inputs]
    y_train = df_train[target]
    X_test = df_test[inputs]
    
    # Use KNN to predict the target value
    # n_neighbors=5 is a robust default for this dataset size
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
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Split data for demonstration: 80% train, 20% test
        split_idx = int(len(rows) * 0.8)
        train_data = rows[:split_idx]
        test_data = [row[:] for row in rows[split_idx:]]
        
        # Mask the goals in test data
        goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for row in test_data:
            for idx in goal_indices:
                row[idx] = "?"
        
        predictions = guess(header, train_data, test_data)
        
        # Calculate average prediction for the customer
        avg_cost = sum(predictions) / len(predictions)
        
        print("Customer Report:")
        print(f"Based on the analysis of {len(train_data)} training records,")
        print(f"the estimated cost for the new setups is approximately {avg_cost:.4f}.")
        print("This estimate is derived using a K-Nearest Neighbors regression model.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
