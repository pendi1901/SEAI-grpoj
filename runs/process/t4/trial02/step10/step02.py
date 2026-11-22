import csv
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from step01 import remember

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows using K-Nearest Neighbors.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify input columns (all columns that are not goals)
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Target is the first goal column
    target_col = goals[0]
    
    # Train KNN regressor
    knn = KNeighborsRegressor(n_neighbors=5)
    knn.fit(df_train[inputs], df_train[target_col])
    
    # Predict for test rows
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
                processed_row = [float(val) for val in row]
                rows.append(processed_row)
        
        # Split data: use 80% for training, 20% as a test set
        split_idx = int(len(rows) * 0.8)
        train_data = rows[:split_idx]
        test_data = [row[:] for row in rows[split_idx:]]
        
        # Mask goals in test data
        goals = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        for row in test_data:
            for g_idx in goals:
                row[g_idx] = "?"
        
        predictions = guess(header, train_data, test_data)
        
        print("Customer Inquiry: Estimated Cost- for test setups")
        print(f"Processed {len(test_data)} test cases.")
        print(f"First 5 estimates: {[round(p, 4) for p in predictions[:5]]}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
