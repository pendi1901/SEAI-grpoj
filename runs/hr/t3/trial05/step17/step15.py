import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on tenure.
    We train a Random Forest to predict 'YearsAtCompany+' and identify
    features with the lowest importance scores.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    target_idx = header.index('YearsAtCompany+')
    feature_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Encode symbolic data
    encoders = {}
    encoded_rows = []
    for row in rows:
        new_row = []
        for i in feature_indices:
            val = row[i]
            if isinstance(val, str):
                if i not in encoders:
                    le = LabelEncoder()
                    le.fit([r[i] for r in rows])
                    encoders[i] = le
                new_row.append(encoders[i].transform([val])[0])
            else:
                new_row.append(val)
        encoded_rows.append(new_row)
    
    X = encoded_rows
    y = [r[target_idx] for r in rows]
    
    # Train a regressor to find feature importance
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    feature_names = [header[i] for i in feature_indices]
    
    # Sort features by importance ascending (least important first)
    sorted_features = sorted(zip(feature_names, importances), key=lambda x: x[1])
    
    # Return the bottom 5 features that have the least impact on tenure
    return [f[0] for f in sorted_features[:5]]

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
            
    unimportant_factors = blame(header, rows)
    
    print("Analysis: Columns with the least impact on 'YearsAtCompany+':")
    for factor in unimportant_factors:
        print(f"- {factor}")
    print("\nThese columns have the lowest predictive power regarding employee tenure.")
    print("Consider stopping collection of these fields to reduce data overhead.")
