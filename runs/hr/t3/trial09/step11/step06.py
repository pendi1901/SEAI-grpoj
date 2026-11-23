import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the performance of a given row relative to the population.
    Returns (p, reason) where p is the percentile rank and reason is a summary.
    """
    # Identify goal columns
    goal_indices = [i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-')]
    input_indices = [i for i, name in enumerate(header) if not (name.endswith('+') or name.endswith('-'))]
    
    # Prepare training data for the first goal (YearsAtCompany+)
    goal_idx = goal_indices[0]
    
    # Encode data
    encoders = {}
    def encode_row(r):
        encoded = []
        for i in input_indices:
            val = r[i]
            if isinstance(val, str):
                if i not in encoders:
                    # Fit encoder on all rows
                    le = LabelEncoder()
                    le.fit([x[i] for x in rows])
                    encoders[i] = le
                encoded.append(encoders[i].transform([val])[0])
            else:
                encoded.append(val)
        return encoded

    X = [encode_row(r) for r in rows]
    y = [r[goal_idx] for r in rows]
    
    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Predict for the target row
    target_x = [encode_row(row)]
    prediction = model.predict(target_x)[0]
    
    # Calculate percentile rank
    better_count = sum(1 for r in rows if r[goal_idx] > prediction)
    p = better_count / len(rows)
    
    reason = f"Based on your team's profile, the predicted tenure of {prediction:.1f} years ranks in the top {int((1-p)*100)}% of our organization."
    
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
    
    # Test with the first row, masking the goal
    test_row = list(rows[0])
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
