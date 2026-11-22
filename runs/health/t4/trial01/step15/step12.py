import csv
from step02 import guess as original_guess

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) using a Random Forest Regressor.
    To answer the customer's question, we compare the performance of a 
    standard forest (n_estimators=100) vs a halved forest (n_estimators=50).
    """
    # The customer asks: "If I halve the size of the forecaster to save run time, 
    # how much worse do the forecasts get?"
    # We implement the requested function signature using the logic from step02.
    return original_guess(header, train, test)

def compare_forecaster_sizes(header, train, test):
    """
    Compares the performance of a standard forest vs a halved forest.
    """
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import LabelEncoder
    import numpy as np

    # Prepare data (reuse logic from step02)
    input_indices = [i for i in range(len(header)) if i >= 3]
    encoders = {}
    for i in input_indices:
        if isinstance(train[0][i], str):
            le = LabelEncoder()
            all_vals = [r[i] for r in train] + [r[i] for r in test if r[i] != "?"]
            le.fit(all_vals)
            encoders[i] = le

    def transform(row):
        return [encoders[i].transform([row[i]])[0] if i in encoders else float(row[i]) for i in input_indices]

    X_train = [transform(r) for r in train]
    y_train = [r[0] for r in train]
    X_test = [transform(r) for r in test]
    y_test = [r[0] for r in test]

    # Train both models
    m1 = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)
    m2 = RandomForestRegressor(n_estimators=50, random_state=42).fit(X_train, y_train)

    # Calculate Mean Absolute Error for both
    mae1 = np.mean(np.abs(m1.predict(X_test) - y_test))
    mae2 = np.mean(np.abs(m2.predict(X_test) - y_test))

    return mae1, mae2

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(val) if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth'] else val for i, val in enumerate(row)]
            rows.append(processed)

    train_data = rows[:700]
    test_data = rows[700:]
    
    mae_full, mae_half = compare_forecaster_sizes(header, train_data, test_data)
    
    print("Impact of halving the forecaster size (N_estimators 100 -> 50):")
    print(f"MAE of full model: {mae_full:.6f}")
    print(f"MAE of halved model: {mae_half:.6f}")
    print(f"The forecast error increases by {((mae_half - mae_full) / mae_full) * 100:.2f}%.")
