import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that best explain short stays (low 'YearsAtCompany+').
    Uses a Random Forest to rank feature importance for predicting tenure.
    """
    goal_name = "YearsAtCompany+"
    goal_idx = header.index(goal_name)
    
    # Identify input columns (exclude goals)
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # Prepare data
    encoders = {}
    X = []
    y = []
    
    for row in rows:
        processed_row = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                if i not in encoders:
                    encoders[i] = LabelEncoder()
                    # Fit on all values for this column
                    encoders[i].fit([r[i] for r in rows])
                processed_row.append(float(encoders[i].transform([val])[0]))
            else:
                processed_row.append(float(val))
        X.append(processed_row)
        y.append(float(row[goal_idx]))
        
    # Train model to find feature importance
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get top 3 features
    importances = sorted(zip(input_indices, model.feature_importances_), key=lambda x: x[1], reverse=True)
    return [header[idx] for idx, imp in importances[:3]]

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

    top_features = blame(header, rows)
    
    print("Analysis: What factors explain short stays (YearsAtCompany+)?")
    print("The most influential input columns are:")
    for feature in top_features:
        print(f"- {feature}")
