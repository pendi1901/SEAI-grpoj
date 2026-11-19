import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows.
    Uses a Random Forest Regressor after encoding symbolic columns.
    """
    # Identify goal columns (ending in + or -)
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_indices[0]
    
    # Prepare data
    X_train = []
    y_train = []
    
    # Encode symbolic columns
    encoders = {}
    for i, col_name in enumerate(header):
        if not col_name[0].isupper():
            le = LabelEncoder()
            # Combine train and test to ensure all categories are seen
            all_vals = [r[i] for r in train] + [r[i] for r in test if r[i] != '?']
            le.fit(all_vals)
            encoders[i] = le

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
        y_train.append(row[target_idx])
    
    X_test = []
    for row in test:
        # Replace '?' with 0 for the target column in test rows
        temp_row = list(row)
        temp_row[target_idx] = 0.0
        X_test.append(transform_row(temp_row))
        
    # Train model
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
    
    # Split: use first 700 for training, next 100 for testing
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal column in test data
    goal_idx = next(i for i, h in enumerate(header) if h.endswith('+'))
    for row in test_data:
        row[goal_idx] = '?'
        
    predictions = guess(header, train_data, test_data)
    
    print("Estimation results for the first 5 test rows:")
    for i in range(min(5, len(predictions))):
        print(f"Row {i+700}: Estimated YearsAtCompany+ = {predictions[i]:.2f}")
