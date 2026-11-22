import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates performance of a row and compares it to the dataset to justify
    why 'bigger/deeper' is not always better.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    input_indices = [i for i, h in enumerate(header) if i not in goal_indices]
    
    # Prepare data for training
    X = []
    y = []
    for r in rows:
        features = []
        for i in input_indices:
            val = r[i]
            if isinstance(val, str):
                features.append(hash(val) % 1000)
            else:
                features.append(float(val))
        X.append(features)
        
        # Aggregate score: (1 - MRE) + ACC + PRED
        mre = r[header.index('MRE-')]
        acc = r[header.index('ACC+')]
        pred = r[header.index('PRED40+')]
        y.append((1.0 - mre) + acc + pred)

    # Train model to predict performance
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)

    # Predict score for the target row
    target_features = []
    for i in input_indices:
        val = row[i]
        if isinstance(val, str):
            target_features.append(hash(val) % 1000)
        else:
            target_features.append(float(val))
    
    target_score = model.predict([target_features])[0]
    
    # Calculate fraction of rows that are worse
    better_than = [s for s in y if target_score > s]
    p = len(better_than) / len(y)
    
    reason = "Bigger setups often lead to overfitting or diminishing returns, meaning a balanced configuration frequently outperforms the maximum possible settings."
    
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = []
            for i, val in enumerate(row):
                if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                    try:
                        processed.append(float(val))
                    except ValueError:
                        processed.append(0.0)
                else:
                    processed.append(val)
            rows.append(processed)

    # Test with a "maxed out" configuration
    # N_estimators=200, Max_depth=20, etc.
    test_row = [0.0, 0.0, 0.0, 200.0, 'squared_error', 1.0, 0.0, 20.0]
    
    p, reason = justify(header, rows, test_row)
    print(f"Performance percentile: {p:.4f}")
    print(f"Reason: {reason}")
