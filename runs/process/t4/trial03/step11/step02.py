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
    inputs = [c for c in header if not (c.endswith('-') or c.endswith('+'))]
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    first_goal = goals[0]
    
    # Prepare X and y
    X_train = df_train[inputs]
    y_train = df_train[first_goal]
    X_test = df_test[inputs]
    
    # Use KNN to predict the first goal
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
                processed_row = [float(val) if val.replace('.','',1).isdigit() or (val.startswith('-') and val[1:].replace('.','',1).isdigit()) else val for val in row]
                rows.append(processed_row)
        
        # Split data: use 80% for training, 20% for testing
        split = int(len(rows) * 0.8)
        train_data = rows[:split]
        test_data = rows[split:]
        
        # Mask the goals in test data to simulate "?"
        goals = [i for i, col in enumerate(header) if col.endswith('-') or col.endswith('+')]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for g in goals:
                new_row[g] = "?"
            masked_test.append(new_row)
            
        predictions = guess(header, train_data, masked_test)
        
        print("Customer Inquiry: Estimated Cost (first goal) for test setups:")
        for i in range(min(5, len(predictions))):
            print(f"Setup {i+1}: Estimated Cost = {predictions[i]:.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
