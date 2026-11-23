import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def blame(header, rows):
    """
    Identifies input columns that best explain why employees have short stays.
    We define 'worst' as the bottom 20% of 'YearsAtCompany+'.
    We use a Random Forest to find feature importances for predicting tenure.
    """
    goal_name = 'YearsAtCompany+'
    goal_idx = header.index(goal_name)
    
    # Filter out goal columns and identify input columns
    input_indices = [i for i, name in enumerate(header) if name != goal_name and not name.endswith(('-', '+'))]
    
    # Sort rows by tenure to find the 'worst' (shortest stay)
    sorted_rows = sorted(rows, key=lambda r: r[goal_idx])
    worst_rows = sorted_rows[:int(len(rows) * 0.2)]
    
    # Prepare data for feature importance
    X = []
    for row in worst_rows:
        features = []
        for i in input_indices:
            val = row[i]
            if isinstance(val, str):
                # Simple label encoding for symbolic columns
                features.append(hash(val) % 1000)
            else:
                features.append(val)
        X.append(features)
    
    y = [row[goal_idx] for row in worst_rows]
    
    # Use Random Forest to find which inputs correlate most with the short tenure
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Get top 3 features
    importances = model.feature_importances_
    indices = importances.argsort()[::-1]
    
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
            
    results = blame(header, rows)
    print("The primary factors explaining short stays in departments are:")
    for factor in results:
        print(f"- {factor}")
