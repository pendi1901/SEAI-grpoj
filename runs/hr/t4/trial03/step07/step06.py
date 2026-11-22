import csv
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
    input_indices = [i for i in range(len(header)) if i != goal_idx]
    encoders = {}
    
    def encode_data(data_rows, is_test=False):
        X = []
        y = []
        for r in data_rows:
            encoded_row = []
            for i in range(len(header)):
                if i == goal_idx:
                    if is_test: continue
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
        return X, y

    X_train, y_train = encode_data(rows)
    
    # Encode test row, skipping the '?' goal
    test_row_encoded = []
    for i in range(len(header)):
        if i == goal_idx: continue
        if isinstance(row[i], str):
            test_row_encoded.append(float(encoders[i].transform([row[i]])[0]))
        else:
            test_row_encoded.append(float(row[i]))
            
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    prediction = model.predict([test_row_encoded])[0]
    
    all_goals = [r[goal_idx] for r in rows]
    if is_maximize:
        better_count = sum(1 for val in all_goals if prediction > val)
    else:
        better_count = sum(1 for val in all_goals if prediction < val)
        
    p = better_count / len(all_goals)
    reason = (f"This team's arrangement ranks in the {p:.2%} percentile of performance, "
              f"as the estimated goal value of {prediction:.2f} outperforms "
              f"{p:.1%} of the existing staff records.")
    
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
