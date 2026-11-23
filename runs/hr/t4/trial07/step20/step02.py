import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates 'YearsAtCompany+' for test rows using a Random Forest Regressor.
    Handles '?' in test data by excluding the goal column from feature encoding.
    """
    goal_idx = header.index('YearsAtCompany+')
    
    # Identify feature indices (all except goal)
    feature_indices = [i for i in range(len(header)) if i != goal_idx]
    
    # Prepare data: encode symbolic columns to numeric
    def encode_data(train_data, test_data):
        encoded_train = []
        encoded_test = []
        
        for i in feature_indices:
            col_train = [row[i] for row in train_data]
            col_test = [row[i] for row in test_data]
            
            if not header[i][0].isupper():
                le = LabelEncoder()
                le.fit([str(x) for x in (col_train + col_test)])
                encoded_train.append(le.transform([str(x) for x in col_train]))
                encoded_test.append(le.transform([str(x) for x in col_test]))
            else:
                encoded_train.append([float(x) for x in col_train])
                encoded_test.append([float(x) for x in col_test])
                
        return list(zip(*encoded_train)), list(zip(*encoded_test))

    X_train, X_test = encode_data(train, test)
    y_train = [row[goal_idx] for row in train]

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict
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

    # Split: 700 train, 100 test
    train_data = rows[:700]
    test_data = rows[700:]
    
    # Mask the goal column in test data
    goal_idx = header.index('YearsAtCompany+')
    masked_test = []
    for row in test_data:
        new_row = list(row)
        new_row[goal_idx] = "?"
        masked_test.append(new_row)
        
    predictions = guess(header, train_data, masked_test)
    
    print("Estimation of 'YearsAtCompany+' for new hires:")
    for i in range(min(5, len(predictions))):
        print(f"Test Row {i}: Predicted {predictions[i]:.2f} years")
