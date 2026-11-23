import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that best explain short stays (low 'YearsAtCompany+').
    We define 'worst' rows as those in the bottom 25% of 'YearsAtCompany+'.
    We use a Random Forest to find feature importances for predicting this goal.
    """
    goal_idx = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')][0]
    
    # Prepare data
    X = []
    y = []
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
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
        y.append(float(row[goal_idx]))

    # Train a regressor to see what drives the goal
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Return the top 3 most influential input columns
    top_features = [header[input_indices[i]] for i in indices[:3]]
    return top_features

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
    
    factors = blame(header, rows)
    
    print("Analysis of short stays:")
    print("The primary factors influencing how long employees stay at the company are:")
    for factor in factors:
        print(f"- {factor}")
    print("\nThese columns show the strongest correlation with tenure duration.")
