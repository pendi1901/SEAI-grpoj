import csv
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goal columns.
    We use a Random Forest Regressor to calculate feature importances and
    return the columns with the lowest importance scores.
    """
    # Identify goal columns
    goal_cols = [c for c in header if c.endswith('+') or c.endswith('-')]
    input_cols = [c for c in header if c not in goal_cols]
    
    df = pd.DataFrame(rows, columns=header)
    
    # Prepare features
    X = df[input_cols].copy()
    
    # Encode symbolic columns
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
        else:
            X[col] = X[col].astype(float).fillna(0)
            
    # We aggregate importance across all goal columns
    total_importances = pd.Series(0.0, index=input_cols)
    
    for goal in goal_cols:
        y = df[goal]
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        total_importances += pd.Series(model.feature_importances_, index=input_cols)
    
    # Normalize and sort
    avg_importances = total_importances / len(goal_cols)
    # Return the columns with the lowest importance (the ones we can stop collecting)
    # We return the bottom 5 features as candidates to stop collecting
    return avg_importances.nsmallest(5).index.tolist()

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
            
    useless_features = blame(header, rows)
    
    print("Based on the analysis, the following columns have the least impact on employee retention goals.")
    print("You may consider stopping the collection of these fields:")
    for feature in useless_features:
        print(f"- {feature}")
