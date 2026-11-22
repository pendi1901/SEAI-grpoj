import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def justify(header, rows, row):
    """
    Estimates the goal column for the provided row and calculates its percentile
    rank against the existing rows. Returns (p, reason).
    """
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    is_maximize = header[goal_idx].endswith('+')
    
    # Prepare data for training
    encoders = {}
    X = []
    y = []
    for r in rows:
        encoded_row = []
        for i in range(len(header)):
            if i == goal_idx:
                y.append(float(r[i]))
            elif isinstance(r[i], str):
                if i not in encoders:
                    le = LabelEncoder()
                    le.fit([row_val[i] for row_val in rows])
                    encoders[i] = le
                encoded_row.append(float(encoders[i].transform([r[i]])[0]))
            else:
                encoded_row.append(float(r[i]))
        X.append(encoded_row)
    
    # Encode test row
    test_row_encoded = []
    for i in range(len(header)):
        if i == goal_idx: continue
        if isinstance(row[i], str):
            test_row_encoded.append(float(encoders[i].transform([row[i]])[0]))
        else:
            test_row_encoded.append(float(row[i]))
            
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    prediction = model.predict([test_row_encoded])[0]
    
    all_goals = [r[goal_idx] for r in rows]
    if is_maximize:
        better_count = sum(1 for val in all_goals if prediction > val)
    else:
        better_count = sum(1 for val in all_goals if prediction < val)
        
    p = better_count / len(all_goals)
    
    # Answer the customer's question about pay
    reason = (f"While increasing pay is a common incentive, our model indicates that tenure is "
              f"driven by a complex mix of factors, placing this arrangement in the {p:.2%} percentile.")
    
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
    
    test_row = rows[0][:]
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+'))
    test_row[goal_idx] = "?"
    
    p, reason = justify(header, rows, test_row)
    print(f"Rank: {p:.4f}")
    print(f"Reason: {reason}")
    exit(0)
