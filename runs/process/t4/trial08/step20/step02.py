import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from step01 import remember

def guess(header, train, test):
    """
    Estimates the first goal column for test rows using K-Nearest Neighbors.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify input columns (those not ending in - or +)
    inputs = [col for col in header if not (col.endswith('-') or col.endswith('+'))]
    
    # Identify the first goal column
    goals = [col for col in header if col.endswith(('-', '+'))]
    target = goals[0]
    
    # Train a KNN regressor
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(df_train[inputs], df_train[target])
    
    # Predict
    predictions = knn.predict(df_test[inputs])
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
        
        # Split data: use 80% for training, 20% for testing
        split_idx = int(len(rows) * 0.8)
        train_data = rows[:split_idx]
        test_data = rows[split_idx:]
        
        # Prepare test data by masking goals
        goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_test.append(new_row)
            
        predictions = guess(header, train_data, masked_test)
        
        # Report results
        print("Customer Inquiry: Estimated Cost and Idle time for test setups.")
        print(f"Processed {len(predictions)} test cases.")
        print(f"First 5 estimated values for the first goal column ({header[goal_indices[0]]}):")
        for i, val in enumerate(predictions[:5]):
            print(f"  Setup {i+1}: {val:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
