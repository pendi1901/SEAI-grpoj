import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import step05

def blame(header, rows):
    """
    Identifies input columns that have the least impact on performance.
    We define 'settings I can leave at default' as those with the lowest 
    feature importance when predicting the utility of the configurations.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    goal_names = {'MRE-', 'ACC+', 'PRED40+'}
    input_indices = [i for i, name in enumerate(header) if name not in goal_names]
    input_names = [header[i] for i in input_indices]

    utilities = [(1.0 - row[mre_idx]) + row[acc_idx] + row[pred_idx] for row in rows]

    X = []
    for row in rows:
        processed = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                processed.append(float(hash(val) % 1000))
            else:
                processed.append(float(val))
        X.append(processed)
    
    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(X, utilities)
    
    importances = rf.feature_importances_
    
    # Sort inputs by importance ascending (least important first)
    sorted_indices = np.argsort(importances)
    
    # Return the names of the least important columns
    return [input_names[i] for i in sorted_indices]

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

    least_important = blame(header, rows)
    
    print("Settings that can be left at factory defaults (least impact on performance):")
    for col in least_important:
        print(f"- {col}")
    print("\nThese settings have the smallest effect on your outcomes.")
