import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that best explain short tenure ('YearsAtCompany+').
    We define 'worst' as the bottom 20% of tenure. We then use a Random Forest
    to find feature importances for predicting tenure, filtering for input columns.
    """
    goal_col = 'YearsAtCompany+'
    goal_idx = header.index(goal_col)
    
    # Filter out goal columns from inputs
    input_indices = [i for i, col in enumerate(header) if not (col.endswith('+') or col.endswith('-'))]
    
    # Encode data
    encoders = {}
    X = []
    y = []
    for row in rows:
        encoded_row = []
        for i, val in enumerate(row):
            if isinstance(val, str):
                if i not in encoders:
                    le = LabelEncoder()
                    le.fit([r[i] for r in rows])
                    encoders[i] = le
                encoded_row.append(float(encoders[i].transform([val])[0]))
            else:
                encoded_row.append(float(val))
        X.append([encoded_row[i] for i in input_indices])
        y.append(encoded_row[goal_idx])
    
    # Train a regressor to find feature importance
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get importances
    importances = model.feature_importances_
    feature_scores = sorted(zip(input_indices, importances), key=lambda x: x[1], reverse=True)
    
    # Return top 3 input columns that explain tenure
    return [header[idx] for idx, score in feature_scores[:3]]

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
    
    important_factors = blame(header, rows)
    
    print("Analysis of factors explaining short tenure:")
    print(f"The primary input columns that influence tenure are: {', '.join(important_factors)}.")
    print("These factors are the strongest predictors of how long an employee stays at the company.")
