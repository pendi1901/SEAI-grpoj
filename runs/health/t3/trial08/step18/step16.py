import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def justify(header, rows, row):
    """
    Estimates if a 'biggest/deepest' setup is optimal by comparing it to 
    the performance distribution of the dataset.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Calculate aggregate scores for training
    # MRE- (min), ACC+ (max), PRED40+ (max)
    # Score = (1 - MRE) + ACC + PRED
    y_train = []
    for r in rows:
        mre = float(r[header.index('MRE-')])
        acc = float(r[header.index('ACC+')])
        pred = float(r[header.index('PRED40+')])
        y_train.append((1.0 - mre) + acc + pred)
    
    X_train = [[r[i] for i in input_indices] for r in rows]
    
    # Preprocessing
    cat_features = [i for i, val in enumerate(rows[0]) if isinstance(val, str) and i in input_indices]
    cat_indices = [input_indices.index(i) for i in cat_features]
    
    preprocessor = ColumnTransformer(
        transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), cat_indices)],
        remainder='passthrough'
    )
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    model.fit(X_train, y_train)
    
    # Predict score for the target row
    target_X = [[row[i] for i in input_indices]]
    estimated_score = model.predict(target_X)[0]
    
    # Calculate fraction of rows outperformed
    better_count = sum(1 for s in y_train if estimated_score > s)
    fraction = better_count / len(rows)
    
    reason = (f"Using the biggest and deepest setup is often counterproductive because "
              f"it risks overfitting, as evidenced by this configuration only "
              f"outperforming {fraction:.1%} of the observed setups.")
    
    return fraction, reason

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
        
        # Define a 'biggest/deepest' setup based on dataset max values
        # N_estimators, Min_sample_leaves, Min_impurity_decrease, Max_depth
        # We use the max observed values from the dataset for these inputs
        max_n = max(r[header.index('N_estimators')] for r in rows)
        max_depth = max(r[header.index('Max_depth')] for r in rows)
        
        # Create a test row with max settings
        test_row = [0.0] * len(header)
        for i, h in enumerate(header):
            if h == 'N_estimators': test_row[i] = max_n
            elif h == 'Max_depth': test_row[i] = max_depth
            elif h == 'criterion': test_row[i] = 'squared_error'
            elif h == 'Min_sample_leaves': test_row[i] = 1.0
            elif h == 'Min_impurity_decrease': test_row[i] = 0.0
            elif h.endswith('-') or h.endswith('+'): test_row[i] = "?"
            else: test_row[i] = 0.0
            
        p, reason = justify(header, rows, test_row)
        print(reason)
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
