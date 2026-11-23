import csv
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using KNN.
    Handles '?' in test rows by ensuring the model only sees numeric/encoded features.
    """
    goal_idx = 0
    # Input features are all columns except the goal column
    input_indices = [i for i in range(len(header)) if i != goal_idx]
    
    X_train = [[row[i] for i in input_indices] for row in train]
    y_train = [float(row[goal_idx]) for row in train]
    
    # For test, we must ensure we don't pass '?' to the model.
    # The pipeline handles categorical encoding, but we must ensure 
    # the input data structure is consistent.
    X_test = [[row[i] for i in input_indices] for row in test]
    
    # Identify categorical columns
    cat_features = [i for i, val in enumerate(train[0]) if isinstance(val, str) and i != goal_idx]
    cat_indices_in_input = [input_indices.index(i) for i in cat_features]
    
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), cat_indices_in_input)],
        remainder='passthrough'
    )
    
    # Halved model (k=2) as requested
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', KNeighborsRegressor(n_neighbors=2))
    ])
    
    model.fit(X_train, y_train)
    return model.predict(X_test).tolist()

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
        y_test = [float(r[0]) for r in test_data]
        
        # Mask goals in test
        for r in test_data:
            r[0] = "?"
            
        # Compare k=5 (full) vs k=2 (halved)
        input_indices = [i for i in range(len(header)) if i != 0]
        cat_features = [i for i, val in enumerate(train_data[0]) if isinstance(val, str) and i != 0]
        cat_indices = [input_indices.index(i) for i in cat_features]
        
        preprocessor = ColumnTransformer([('cat', OneHotEncoder(handle_unknown='ignore'), cat_indices)], remainder='passthrough')
        
        m5 = Pipeline([('p', preprocessor), ('r', KNeighborsRegressor(n_neighbors=5))]).fit(
            [[r[i] for i in input_indices] for r in train_data], [float(r[0]) for r in train_data])
        m2 = Pipeline([('p', preprocessor), ('r', KNeighborsRegressor(n_neighbors=2))]).fit(
            [[r[i] for i in input_indices] for r in train_data], [float(r[0]) for r in train_data])
        
        err5 = np.mean(np.abs(m5.predict([[r[i] for i in input_indices] for r in test_data]) - y_test))
        err2 = np.mean(np.abs(m2.predict([[r[i] for i in input_indices] for r in test_data]) - y_test))
        
        print(f"Average error with full forecaster (k=5): {err5:.4f}")
        print(f"Average error with halved forecaster (k=2): {err2:.4f}")
        print(f"The forecast accuracy degrades by approximately {((err2/err5)-1)*100:.2f}% when halving the model size.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
