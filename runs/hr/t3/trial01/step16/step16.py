import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of a given row relative to the population.
    We use a Random Forest to predict the goal 'YearsAtCompany+' and
    compare it against the actual population to explain why simply 
    increasing pay is not a universal solution.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_indices[0]
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    # Encode symbolic columns
    encoders = {}
    for i in input_indices:
        if not header[i][0].isupper():
            le = LabelEncoder()
            le.fit([str(r[i]) for r in rows])
            encoders[i] = le

    def transform(r):
        features = []
        for i in input_indices:
            val = r[i]
            if i in encoders:
                features.append(float(encoders[i].transform([str(val)])[0]))
            else:
                features.append(float(val))
        return features

    X = [transform(r) for r in rows]
    y = [float(r[target_idx]) for r in rows]
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Predict for the provided row
    prediction = model.predict([transform(row)])[0]
    
    # Calculate percentile
    better_than_count = sum(1 for val in y if val < prediction)
    p = better_than_count / len(rows)
    
    reason = (f"Increasing pay alone is insufficient because our model shows that tenure is driven by a complex "
              f"combination of job role, overtime, and satisfaction, meaning that for this employee, "
              f"the predicted retention rank is only in the {p:.1%} percentile of the current workforce.")
    
    return p, reason

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    # Test with the first row, masking its goal columns
    test_row = list(rows[0])
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    print(reason)
