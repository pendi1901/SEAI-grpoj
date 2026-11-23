import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from step01 import remember

def guess(header, train, test):
    """
    Estimates the first goal column for each test row using K-Nearest Neighbors
    based on the input columns (non-goal columns).
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify goal columns and input columns
    goals = [col for col in header if col.endswith(('-', '+'))]
    inputs = [col for col in header if col not in goals]
    
    # Target is the first goal column
    target = goals[0]
    
    # Train KNN on input columns to predict the target
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(df_train[inputs], df_train[target])
    
    # Predict for test rows
    predictions = model.predict(df_test[inputs])
    
    return predictions.tolist()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row]
                rows.append(processed_row)
        
        # Split data: use 80% for training, 20% for testing simulation
        split_idx = int(len(rows) * 0.8)
        train_data = rows[:split_idx]
        test_data = [row[:] for row in rows[split_idx:]]
        
        # Mask the goals in test data
        goals = [col for col in header if col.endswith(('-', '+'))]
        for row in test_data:
            for col in goals:
                row[header.index(col)] = "?"
        
        predictions = guess(header, train_data, test_data)
        
        print("Customer Inquiry: Estimated Cost (first goal) for test setups:")
        for i, val in enumerate(predictions[:5]):
            print(f"  Setup {i+1}: {val:.4f}")
        print("  ...")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
