import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    To answer the customer's question about cutting overtime in Sales,
    we train a model on the existing data and then predict the outcome
    for test rows where we manually set 'overTime' to 'No' for 'Sales' employees.
    """
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+') or name.endswith('-'))
    feature_indices = [i for i in range(len(header)) if i != goal_idx]
    
    # Encode symbolic columns
    encoders = {}
    def encode_data(data_rows, is_train=False):
        encoded = []
        for row in data_rows:
            new_row = []
            for i in feature_indices:
                val = row[i]
                if isinstance(val, str):
                    if i not in encoders:
                        encoders[i] = LabelEncoder().fit([r[i] for r in train])
                    try:
                        new_row.append(float(encoders[i].transform([val])[0]))
                    except ValueError:
                        new_row.append(0.0)
                else:
                    new_row.append(float(val))
            encoded.append(new_row)
        return encoded

    X_train = encode_data(train, is_train=True)
    y_train = [row[goal_idx] for row in train]
    
    # Prepare test data: simulate cutting overtime for Sales
    test_modified = []
    ot_idx = header.index('overTime')
    dept_idx = header.index('department')
    for row in test:
        new_row = list(row)
        if new_row[dept_idx] == 'Sales':
            new_row[ot_idx] = 'No'
        test_modified.append(new_row)
        
    X_test = encode_data(test_modified)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model.predict(X_test).tolist()

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
    
    # Use all data to train, then predict on the same data to see the "impact"
    # of the policy change (cutting overtime in Sales)
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    test_rows = [list(r) for r in rows]
    for r in test_rows:
        r[goal_idx] = "?"
        
    predictions = guess(header, rows, test_rows)
    
    # Compare average tenure before and after simulated policy change
    original_avg = sum(r[goal_idx] for r in rows) / len(rows)
    new_avg = sum(predictions) / len(predictions)
    
    print("Customer Analysis: Impact of cutting overtime in Sales on employee tenure.")
    print(f"Average tenure (current): {original_avg:.2f} years")
    print(f"Average tenure (if overtime is cut in Sales): {new_avg:.2f} years")
    print("Conclusion: The model suggests that eliminating overtime for Sales staff "
          f"{'increases' if new_avg > original_avg else 'decreases'} average tenure.")
