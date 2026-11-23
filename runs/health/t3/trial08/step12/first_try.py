import csv
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    Compares performance of a standard KNN (k=5) vs a 'halved' version (k=2).
    """
    goal_idx = 0
    input_indices = [i for i in range(len(header)) if i != goal_idx]
    
    X_train = [[row[i] for i in input_indices] for row in train]
    y_train = [row[goal_idx] for row in train]
    X_test = [[row[i] for i in input_indices] for row in test]
    
    cat_features = [i for i, val in enumerate(train[0]) if isinstance(val, str)]
    cat_indices_in_input = [input_indices.index(i) for i in cat_features if i in input_indices]
    
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), cat_indices_in_input)],
        remainder='passthrough'
    )
    
    # Standard model (k=5)
    model_full = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', KNeighborsRegressor(n_neighbors=5))
    ])
    
    # Halved model (k=2)
    model_half = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', KNeighborsRegressor(n_neighbors=2))
    ])
    
    model_full.fit(X_train, y_train)
    model_half.fit(X_train, y_train)
    
    preds_full = model_full.predict(X_test)
    preds_half = model_half.predict(X_test)
    
    # Return the halved model predictions as requested by the function signature
    return preds_half.tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
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
        
        # Split: train on 700, test on 100
        train_data = rows[:700]
        test_data = [list(r) for r in rows[700:800]]
        for r in test_data:
            r[0] = "?"
            
        # Calculate impact of halving k from 5 to 2
        goal_idx = 0
        input_indices = [i for i in range(len(header)) if i != goal_idx]
        X_train = [[row[i] for i in input_indices] for row in train_data]
        y_train = [row[goal_idx] for row in train_data]
        X_test = [[row[i] for i in input_indices] for row in test_data]
        y_test = [row[goal_idx] for row in rows[700:800]]
        
        cat_features = [i for i, val in enumerate(train_data[0]) if isinstance(val, str)]
        cat_indices = [input_indices.index(i) for i in cat_features if i in input_indices]
        
        preprocessor = ColumnTransformer([('cat', OneHotEncoder(handle_unknown='ignore'), cat_indices)], remainder='passthrough')
        
        m5 = Pipeline([('p', preprocessor), ('r', KNeighborsRegressor(n_neighbors=5))]).fit(X_train, y_train)
        m2 = Pipeline([('p', preprocessor), ('r', KNeighborsRegressor(n_neighbors=2))]).fit(X_train, y_train)
        
        err5 = np.mean(np.abs(m5.predict(X_test) - y_test))
        err2 = np.mean(np.abs(m2.predict(X_test) - y_test))
        
        print(f"Average error with full forecaster (k=5): {err5:.4f}")
        print(f"Average error with halved forecaster (k=2): {err2:.4f}")
        print(f"The forecast accuracy degrades by approximately {((err2/err5)-1)*100:.2f}% when halving the model size.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
