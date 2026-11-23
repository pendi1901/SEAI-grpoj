import csv
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Predicts the first goal column (MRE-) for test rows.
    Compares a full-sized model vs a halved-size model to answer the customer's question.
    """
    goal_idx = 0
    symbolic_indices = [i for i, val in enumerate(train[0]) if isinstance(val, str)]
    
    encoders = {}
    for i in symbolic_indices:
        le = LabelEncoder()
        all_vals = [r[i] for r in train] + [r[i] for r in test if r[i] != "?"]
        le.fit(all_vals)
        encoders[i] = le

    def transform(row, is_test=False):
        new_row = []
        for i, val in enumerate(row):
            if i == goal_idx:
                continue
            if i in symbolic_indices:
                new_row.append(encoders[i].transform([val])[0])
            else:
                # If it's a numeric column that is '?', we treat as 0
                val_float = 0.0 if val == "?" else float(val)
                new_row.append(val_float)
        return new_row

    X_train = [transform(row) for row in train]
    y_train = [row[goal_idx] for row in train]
    X_test = [transform(row, is_test=True) for row in test]

    # Train full model
    model_full = RandomForestRegressor(n_estimators=100, random_state=42)
    model_full.fit(X_train, y_train)
    
    # Train halved model
    model_half = RandomForestRegressor(n_estimators=50, random_state=42)
    model_half.fit(X_train, y_train)

    preds_full = model_full.predict(X_test)
    preds_half = model_half.predict(X_test)
    
    # Calculate average absolute difference
    diff = sum(abs(a - b) for a, b in zip(preds_full, preds_half)) / len(preds_full)
    
    # Store the difference in a side channel
    guess.last_diff = diff
    
    return preds_half.tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for i, val in enumerate(row):
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        split = int(len(rows) * 0.8)
        train_data = rows[:split]
        test_data = [r[:] for r in rows[split:]]
        for r in test_data:
            r[0] = "?"
        
        predictions = guess(header, train_data, test_data)
        
        print(f"Analysis complete.")
        print(f"Halving the forecaster size results in an average prediction shift of {guess.last_diff:.6f} in MRE-.")
        print(f"First 5 predictions: {[round(p, 4) for p in predictions[:5]]}")
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
