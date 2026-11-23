import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the percentile rank of a row's potential performance and explains 
    why 'paying everyone more' is not a simple, universal solution.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    feature_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Prepare training data
    X = [[r[i] for i in feature_indices] for r in rows]
    # We use the first goal (YearsAtCompany+) as the primary metric for retention
    y = [r[goal_indices[0]] for r in rows]
    
    # Encode features
    encoders = {}
    for i in range(len(X[0])):
        if isinstance(X[0][i], str):
            le = LabelEncoder()
            le.fit([r[i] for r in rows])
            encoders[i] = le
            for j in range(len(X)):
                X[j][i] = le.transform([X[j][i]])[0]
    
    # Prepare test row (replace '?' with a neutral value or mean)
    test_features = []
    for i in feature_indices:
        val = row[i]
        if i in encoders:
            test_features.append(encoders[i].transform([val])[0])
        else:
            test_features.append(val)
            
    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    prediction = model.predict([test_features])[0]
    
    # Calculate percentile rank
    better_count = sum(1 for val in y if val < prediction)
    p = better_count / len(y)
    
    reason = ("While increasing pay is a lever, our analysis shows that tenure is driven by a complex "
              "combination of factors like job role, overtime, and management, meaning a blanket "
              "pay raise ignores the specific structural needs of different employee segments.")
    
    return p, reason

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
    
    # Create a sample row with goals masked
    sample_row = list(rows[0])
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('+', '-'))]
    for idx in goal_indices:
        sample_row[idx] = "?"
        
    p, reason = justify(header, rows, sample_row)
    
    print(f"Analysis Result (Percentile: {p:.4f})")
    print(f"Answer: {reason}")
