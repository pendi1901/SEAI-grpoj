import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a Random Forest Regressor.
    """
    # Identify goal column (first column ending in '+' or '-')
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('+') or name.endswith('-'):
            goal_idx = i
            break
    
    # Prepare data
    X_train = []
    y_train = []
    
    # Encode symbolic columns
    encoders = {}
    for i, name in enumerate(header):
        if not name[0].isupper():
            encoders[i] = LabelEncoder()
            # Fit on combined data to ensure all labels are seen
            all_vals = [r[i] for r in train] + [r[i] for r in test if r[i] != '?']
            encoders[i].fit(all_vals)

    def transform_row(row):
        new_row = []
        for i, val in enumerate(row):
            if i in encoders:
                new_row.append(encoders[i].transform([val])[0])
            else:
                new_row.append(float(val))
        return new_row

    for row in train:
        X_train.append(transform_row(row))
        y_train.append(row[goal_idx])

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict
    results = []
    for row in test:
        # For test rows, replace '?' with a dummy value (e.g., 0) for the goal column
        test_row = list(row)
        test_row[goal_idx] = 0.0
        X_test = transform_row(test_row)
        results.append(float(model.predict([X_test])[0]))
        
    return results

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

    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:800]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, name in enumerate(header) if name.endswith('+'))
    for row in test_data:
        row[goal_idx] = "?"

    predictions = guess(header, train_data, test_data)
    
    print(f"Estimated 'YearsAtCompany+' for first 5 test cases:")
    for i in range(min(5, len(predictions))):
        print(f"Row {i+1}: {predictions[i]:.2f} years")
