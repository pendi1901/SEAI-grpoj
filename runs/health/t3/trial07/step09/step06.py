import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

def justify(header, rows, row):
    """
    Estimates the performance of 'row' using a RandomForestRegressor and
    compares it to all other rows to determine its percentile rank.
    """
    # Identify goal and input columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i, name in enumerate(header) if not name.endswith(('-', '+'))]
    
    # Prepare training data
    X = []
    y = []
    for r in rows:
        # We use the first goal as the primary metric for justification
        target_idx = goal_indices[0]
        
        # Encode symbolic inputs
        features = []
        for i in input_indices:
            val = r[i]
            features.append(hash(val) if isinstance(val, str) else val)
        X.append(features)
        y.append(r[target_idx])
    
    # Train model to estimate the goal for the target row
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Predict for the target row
    target_features = []
    for i in input_indices:
        val = row[i]
        target_features.append(hash(val) if isinstance(val, str) else val)
    
    estimated_val = model.predict([target_features])[0]
    
    # Compare against all rows
    better_count = 0
    goal_direction = -1 if header[goal_indices[0]].endswith('-') else 1
    
    for r in rows:
        actual_val = r[goal_indices[0]]
        if goal_direction == -1: # Minimize
            if estimated_val < actual_val:
                better_count += 1
        else: # Maximize
            if estimated_val > actual_val:
                better_count += 1
                
    p = better_count / len(rows)
    reason = f"This setup is estimated to outperform {p:.1%} of all configurations based on its predicted primary objective score."
    
    return p, reason

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    processed_row.append(float(val))
                else:
                    processed_row.append(val)
            rows.append(processed_row)
    
    # Pick a sample row to justify (e.g., the last one)
    test_row = rows[-1][:]
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(f"Percentile: {p}")
    print(f"Reason: {reason}")
