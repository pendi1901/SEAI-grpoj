import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that have the least influence on the goal 
    'YearsAtCompany+'. Columns with low feature importance are candidates 
    for removal.
    """
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    input_indices = [i for i, col in enumerate(header) if not (col.endswith('+') or col.endswith('-'))]
    
    encoders = {}
    X = []
    y = []
    for row in rows:
        encoded_row = []
        for i in range(len(header)):
            if i == goal_idx:
                y.append(float(row[i]))
            elif isinstance(row[i], str):
                if i not in encoders:
                    le = LabelEncoder()
                    le.fit([r[i] for r in rows])
                    encoders[i] = le
                encoded_row.append(float(encoders[i].transform([row[i]])[0]))
            else:
                encoded_row.append(float(row[i]))
        X.append([encoded_row[i] for i in input_indices])
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get importances and sort by score ascending (least important first)
    importances = model.feature_importances_
    feature_scores = sorted(zip(input_indices, importances), key=lambda x: x[1])
    
    # Return the names of the 5 least important input columns
    return [header[idx] for idx, score in feature_scores[:5]]

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
    
    print("Analysis: Columns that have little to no impact on tenure:")
    print(f"You may consider stopping the collection of these columns: {', '.join(unimportant_factors)}.")
    print("These columns showed the lowest predictive power regarding employee retention.")
    exit(0)
