import csv
from step01 import remember
from sklearn.neighbors import KNeighborsRegressor
import numpy as np

def guess(header, train, test):
    """
    Estimates the first goal column for test rows using K-Nearest Neighbors
    based on the input columns (non-goal columns).
    """
    # Identify goal indices
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    first_goal_idx = goal_indices[0]
    
    # Identify input columns (all columns that are not goals)
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Prepare training data
    X_train = [[row[i] for i in input_indices] for row in train]
    y_train = [row[first_goal_idx] for row in train]
    
    # Prepare test data
    X_test = [[row[i] for i in input_indices] for row in test]
    
    # Use KNN to estimate the goal value
    # k=5 is a standard heuristic for small datasets
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X_train, y_train)
    
    return model.predict(X_test).tolist()

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
        
        # Mask goals in test data
        goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_test.append(new_row)
            
        predictions = guess(header, train_data, masked_test)
        
        print("Estimation complete.")
        print(f"Estimated values for the first goal column ({header[goal_indices[0]]}) for the first 5 test rows:")
        for i in range(min(5, len(predictions))):
            print(f"Row {i+1}: {predictions[i]:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
