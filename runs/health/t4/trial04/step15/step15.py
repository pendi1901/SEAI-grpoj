import csv
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def blame(header, rows):
    """
    Identifies which input columns have the least impact on performance.
    We define 'badness' as the inverse of the score.
    Columns with low feature importance in a Random Forest are 
    candidates for 'factory default' settings.
    """
    mre_idx = header.index('MRE-')
    acc_idx = header.index('ACC+')
    pred_idx = header.index('PRED40+')
    
    # Input columns are those not ending in - or +
    input_indices = [i for i, h in enumerate(header) if '-' not in h and '+' not in h]
    
    # Calculate badness score: higher badness = worse performance
    badness = []
    for row in rows:
        # Score = (1 - MRE) + ACC + PRED40. Badness = 3 - Score
        score = (1.0 - float(row[mre_idx])) + float(row[acc_idx]) + float(row[pred_idx])
        badness.append(3.0 - score)
        
    # Prepare X matrix
    X = []
    for row in rows:
        features = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple hash for symbolic columns
                features.append(hash(val))
            else:
                features.append(float(val))
        X.append(features)
        
    # Train a regressor to predict badness
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, badness)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Pair names with importance
    ranked = sorted(zip([header[i] for i in input_indices], importances), 
                    key=lambda x: x[1])
    
    # Return the names of the input columns with the lowest importance
    return [item[0] for item in ranked]

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
            rows.append(processed_row)
            
    safe_settings = blame(header, rows)
    
    print("Analysis of settings that can be left at factory defaults:")
    print("These settings have the least impact on performance (ranked from least to most important):")
    print(", ".join(safe_settings))
    print("\nYou can safely leave the first few settings at their defaults without hurting outcomes.")
