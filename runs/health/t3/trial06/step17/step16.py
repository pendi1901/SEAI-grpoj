import csv
from sklearn.ensemble import RandomForestRegressor

def get_utility(header, row):
    """Calculates a normalized utility score for a row."""
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Normalize goals to [0, 1]
    mre = min(1.0, max(0.0, row[mre_idx]))
    acc = min(1.0, max(0.0, row[acc_idx]))
    pred = min(1.0, max(0.0, row[pred_idx]))
    
    return (1.0 - mre) + acc + pred

def justify(header, rows, row):
    """
    Estimates performance of a 'big' setup and compares it to the dataset.
    Returns (p, reason) where p is the fraction of rows outperformed.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    input_indices = [i for i, h in enumerate(header) if not (h.endswith('-') or h.endswith('+'))]
    
    # Prepare training data
    X_train = []
    y_train = []
    for r in rows:
        features = []
        for i in input_indices:
            val = r[i]
            features.append(hash(val) % 1000 if isinstance(val, str) else val)
        X_train.append(features)
        y_train.append([r[g] for g in goal_indices])
    
    # Train model for goals
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict for the input row
    test_features = []
    for i in input_indices:
        val = row[i]
        test_features.append(hash(val) % 1000 if isinstance(val, str) else val)
    
    predicted_goals = model.predict([test_features])[0]
    
    # Calculate utility of the predicted row
    full_row = [0.0] * len(header)
    for i, g_idx in enumerate(goal_indices):
        full_row[g_idx] = predicted_goals[i]
    for i, idx in enumerate(input_indices):
        full_row[idx] = row[idx]
        
    target_utility = get_utility(header, full_row)
    
    # Compare against all rows
    better_count = sum(1 for r in rows if target_utility > get_utility(header, r))
    p = better_count / len(rows)
    
    reason = "Using the biggest, deepest setup often leads to overfitting or diminishing returns, meaning it only outperforms {:.1%} of the configurations in our dataset.".format(p)
    return (p, reason)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for line in reader:
            processed_row = []
            for i, val in enumerate(line):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
    
    # Define a "big, deep" setup: Max N_estimators, Max depth
    # Based on the data, N_estimators goes up to 200, Max_depth up to 20
    big_setup = ["?"] * 3 + [200.0, 'squared_error', 1.0, 1.0, 20.0]
    
    p, reason = justify(header, rows, big_setup)
    print(reason)
