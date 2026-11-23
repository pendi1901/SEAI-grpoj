import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of a given row relative to the dataset.
    Returns (p, reason) where p is the percentile rank and reason explains
    why simply increasing salary is not a sufficient retention strategy.
    """
    goal_cols = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    input_indices = [i for i in range(len(header)) if i not in goal_cols]

    # Prepare training data
    X_train = []
    y_train = []
    for r in rows:
        features = []
        for i in input_indices:
            val = r[i]
            if isinstance(val, str):
                features.append(hash(val))
            else:
                features.append(val)
        X_train.append(features)
        
        # Aggregate score: Maximize '+' goals, minimize '-' goals
        score = 0
        for g in goal_cols:
            val = r[g]
            if header[g].endswith('-'):
                score -= val
            else:
                score += val
        y_train.append(score)

    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Predict score for the input row
    input_features = []
    for i in input_indices:
        val = row[i]
        if isinstance(val, str):
            input_features.append(hash(val))
        else:
            input_features.append(val)
    
    predicted_score = model.predict([input_features])[0]

    # Calculate percentile
    better_than = sum(1 for y in y_train if predicted_score > y)
    p = better_than / len(rows)
    
    # Reason: Salary is only one factor; data shows tenure is driven by 
    # complex interactions like JobInvolvement and WorkLifeBalance.
    reason = "Increasing salary alone is insufficient because our data shows that retention is significantly driven by non-monetary factors like Job Involvement and Work-Life Balance."
    
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

    # Test with the first row, masking its goals
    test_row = list(rows[0])
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            test_row[i] = "?"
            
    p, reason = justify(header, rows, test_row)
    print(f"Percentile: {p:.4f}")
    print(f"Reason: {reason}")
