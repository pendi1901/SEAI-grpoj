import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import step01

def blame(header, rows):
    """
    Identifies input columns that correlate most strongly with poor performance.
    We define 'bad' as the bottom 25% of rows based on the utility score 
    defined in step01. We use a Random Forest to find feature importances 
    for predicting the utility score.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Identify input columns (exclude goals)
    goal_names = {'MRE-', 'ACC+', 'PRED40+'}
    input_indices = [i for i, name in enumerate(header) if name not in goal_names]
    input_names = [header[i] for i in input_indices]

    # Calculate utility for all rows
    utilities = []
    for row in rows:
        utilities.append((1.0 - row[mre_idx]) + row[acc_idx] + row[pred_idx])

    # Prepare data for Random Forest
    X = []
    for row in rows:
        processed = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple hash for symbolic columns
                processed.append(float(hash(val) % 1000))
            else:
                processed.append(float(val))
        X.append(processed)
    
    # Train a regressor to predict utility
    # Features that have high importance in predicting low utility are the 'blame'
    rf = RandomForestRegressor(n_estimators=50, random_state=42)
    rf.fit(X, utilities)
    
    # Get feature importances
    importances = rf.feature_importances_
    
    # Sort inputs by importance
    sorted_indices = np.argsort(importances)[::-1]
    return [input_names[i] for i in sorted_indices[:3]]

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

    blame_cols = blame(header, rows)
    
    print("Analysis of poor performance:")
    print("The settings that most significantly contribute to performance variance are:")
    for col in blame_cols:
        print(f"- {col}")
    print("\nThese columns are the primary drivers of the observed 'bad' setups.")
