import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goal columns.
    We train a Random Forest to predict the goal and identify features with
    the lowest importance scores.
    """
    # Identify goal columns and input columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # We focus on the first goal column for simplicity
    target_idx = goal_indices[0]
    
    # Prepare data
    X = []
    y = []
    encoders = {}
    
    for i in input_indices:
        if not header[i][0].isupper():
            le = LabelEncoder()
            le.fit([str(row[i]) for row in rows])
            encoders[i] = le

    for row in rows:
        features = []
        for i in input_indices:
            if i in encoders:
                features.append(encoders[i].transform([str(row[i])])[0])
            else:
                features.append(float(row[i]))
        X.append(features)
        y.append(float(row[target_idx]))

    # Train a regressor to determine feature importance
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Pair feature names with their importance
    feature_importances = []
    for i, idx in enumerate(input_indices):
        feature_importances.append((header[idx], importances[i]))
    
    # Sort by importance ascending (least important first)
    feature_importances.sort(key=lambda x: x[1])
    
    # Return the names of the columns with the lowest importance
    # We return the bottom 5 columns as candidates for removal
    return [name for name, imp in feature_importances[:5]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
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
    
    useless_columns = blame(header, rows)
    
    print("Analysis: Columns that have little impact on employee retention.")
    print("The following columns could potentially be removed from data collection:")
    for col in useless_columns:
        print(f"- {col}")
    print("\nLogic: These columns showed the lowest feature importance in predicting tenure.")
