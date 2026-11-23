import csv
from sklearn.ensemble import RandomForestRegressor
import numpy as np

def guess(header, train, test):
    """
    Estimates the first goal column ('YearsAtCompany+') for test rows
    using a Random Forest Regressor based on input columns.
    """
    # Identify goal columns (ending in + or -)
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    target_idx = goal_indices[0]
    
    # Identify input columns (those not ending in + or -)
    input_indices = [i for i in range(len(header)) if i not in goal_indices]
    
    def encode(data):
        """Simple encoding: numeric stays, symbolic becomes categorical index."""
        encoded = []
        for row in data:
            new_row = []
            for i, val in enumerate(row):
                if isinstance(val, str):
                    # Convert string to unique integer
                    new_row.append(hash(val) % 1000)
                else:
                    new_row.append(val)
            encoded.append(new_row)
        return np.array(encoded)

    # Prepare training data
    X_train = encode([ [row[i] for i in input_indices] for row in train ])
    y_train = [row[target_idx] for row in train]
    
    # Prepare test data
    X_test = encode([ [row[i] for i in input_indices] for row in test ])
    
    # Train model
    model = RandomForestRegressor(n_estimators=50, random_state=42)
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
    test_data = rows[700:800]
    
    # Mask goals in test data
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    for row in test_data:
        for idx in goal_indices:
            row[idx] = "?"
            
    predictions = guess(header, train_data, test_data)
    
    print("Estimation for 'YearsAtCompany+' (First 5 test rows):")
    for i in range(min(5, len(predictions))):
        print(f"Row {i+700}: Predicted {predictions[i]:.2f} years")
