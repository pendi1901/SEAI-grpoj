import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a 
    RandomForestRegressor, handling masked values ('?') correctly.
    """
    goal_idx = 0  # MRE-
    symbolic_cols = [i for i, col in enumerate(header) if col == 'criterion']
    
    # Prepare encoders
    encoders = {}
    all_data = train + test
    for col_idx in symbolic_cols:
        le = LabelEncoder()
        # Only fit on non-masked values
        valid_vals = [str(row[col_idx]) for row in all_data if row[col_idx] != "?"]
        le.fit(valid_vals)
        encoders[col_idx] = le

    def transform_row(row, is_train=True):
        new_row = []
        for i, val in enumerate(row):
            # Skip goal columns if they are masked
            if i < 3: 
                continue
            if i in symbolic_cols:
                new_row.append(encoders[i].transform([str(val)])[0])
            else:
                new_row.append(float(val))
        return new_row

    X_train = [transform_row(row) for row in train]
    y_train = [row[goal_idx] for row in train]
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict
    X_test = [transform_row(row) for row in test]
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
    
    # Split: 80% train, 20% test
    split = int(len(rows) * 0.8)
    train_data = rows[:split]
    test_data = [r[:] for r in rows[split:]]
    
    # Mask goals in test data
    for row in test_data:
        for i in range(3): # MRE-, ACC+, PRED40+
            row[i] = "?"
            
    predictions = guess(header, train_data, test_data)
    
    print(f"Estimated MRE- for the first 5 test cases:")
    for i in range(min(5, len(predictions))):
        print(f"Row {split + i}: {predictions[i]:.4f}")
