import csv
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

def guess(header, train, test):
    """
    Estimates the first goal column value for each test row using K-Nearest Neighbors.
    """
    df_train = pd.DataFrame(train, columns=header)
    df_test = pd.DataFrame(test, columns=header)
    
    # Identify goal columns and input columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    inputs = [c for c in header if c not in goals]
    
    # Target is the first goal column
    target_col = goals[0]
    
    # Prepare training data (only numeric inputs)
    X_train = df_train[inputs].select_dtypes(include=['number'])
    y_train = df_train[target_col]
    
    # Prepare test data
    X_test = df_test[inputs].select_dtypes(include=['number'])
    
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
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        # Split data: use first 700 for training, next 100 for testing
        train_data = rows[:700]
        test_data = rows[700:800]
        
        # Mask goals in test data
        goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
        masked_test = []
        for row in test_data:
            new_row = list(row)
            for idx in goal_indices:
                new_row[idx] = "?"
            masked_test.append(new_row)
            
        predictions = guess(header, train_data, masked_test)
        
        print("Customer Inquiry: Estimated Cost (First Goal Column)")
        print("-" * 50)
        print(f"{'Row Index':<12} | {'Estimated Cost':<15}")
        print("-" * 50)
        for i, val in enumerate(predictions[:10]):
            print(f"{i+700:<12} | {val:.4f}")
        print("...")
        print(f"Total estimates generated: {len(predictions)}")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
