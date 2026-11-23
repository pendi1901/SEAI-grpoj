import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of a given row relative to the dataset.
    Returns (p, reason) where p is the percentile rank and reason is the explanation.
    """
    # Identify goal columns
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    # Prepare data for training a regressor to estimate the goal values
    # We use all rows that have complete data
    X = []
    y = []
    
    # Encoders for symbolic columns
    encoders = {}
    for i, h in enumerate(header):
        if not h[0].isupper() and i not in goal_indices:
            encoders[i] = LabelEncoder()
            encoders[i].fit([r[i] for r in rows])

    def process_row(r):
        features = []
        for i, val in enumerate(r):
            if i in encoders:
                features.append(float(encoders[i].transform([val])[0]))
            else:
                features.append(float(val))
        return features

    # Train a model to predict the first goal (YearsAtCompany+)
    target_idx = goal_indices[0]
    X = [process_row(r) for r in rows]
    y = [r[target_idx] for r in rows]
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Predict the value for the input row
    input_features = process_row(row)
    prediction = model.predict([input_features])[0]
    
    # Calculate how many rows are worse than this prediction
    # Since YearsAtCompany+ is a "maximize" goal, higher is better
    better_than_count = sum(1 for r in rows if r[target_idx] < prediction)
    p = better_than_count / len(rows)
    
    reason = (f"This employee's estimated tenure of {prediction:.1f} years ranks them "
              f"in the {p:.0%} percentile of the company's retention performance.")
    
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
    
    # Test with the last row as an example
    test_row = rows[-1][:]
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
