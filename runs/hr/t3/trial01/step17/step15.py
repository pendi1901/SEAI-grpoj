import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least impact on predicting 
    tenure ('YearsAtCompany+'). Columns with low feature importance 
    are candidates for removal.
    """
    # Identify goal column
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    
    # Identify input columns (exclude goals)
    input_indices = [i for i in range(len(header)) if not (header[i].endswith('+') or header[i].endswith('-'))]
    
    # Encode symbolic columns
    encoders = {}
    for i in input_indices:
        if not header[i][0].isupper():
            le = LabelEncoder()
            le.fit([str(r[i]) for r in rows])
            encoders[i] = le

    X = []
    y = []
    for row in rows:
        features = []
        for i in input_indices:
            val = row[i]
            if i in encoders:
                features.append(float(encoders[i].transform([str(val)])[0]))
            else:
                features.append(float(val))
        X.append(features)
        y.append(float(row[goal_idx]))

    # Train model to predict tenure
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Get feature importances
    importances = model.feature_importances_
    
    # Map importances back to column names
    feature_map = []
    for idx, imp in zip(input_indices, importances):
        feature_map.append((header[idx], imp))
    
    # Sort by importance ascending (least important first)
    feature_map.sort(key=lambda x: x[1])
    
    # Return the names of the 5 least influential columns
    return [item[0] for item in feature_map[:5]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = []
    
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
            
    useless_factors = blame(header, rows)
    
    print("Analysis: Which data points have little impact on retention?")
    print("The following columns have the lowest predictive power regarding 'YearsAtCompany+':")
    for factor in useless_factors:
        print(f"- {factor}")
    print("\nThese columns contribute the least to our tenure model and are candidates for removal.")
