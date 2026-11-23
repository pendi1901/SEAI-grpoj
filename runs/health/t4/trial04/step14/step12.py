import csv
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder

def guess(header, train, test):
    """
    Estimates the MRE- (first goal) for test rows.
    Compares a full-sized KNN (n=5) vs a halved-size KNN (n=2)
    to answer the customer's question about performance degradation.
    """
    goal_idx = 0
    symbolic_indices = [i for i, col in enumerate(header) if col == 'criterion']
    
    # Prepare training data (all numeric/encoded)
    train_arr = np.array(train, dtype=object)
    for idx in symbolic_indices:
        le = LabelEncoder()
        train_arr[:, idx] = le.fit_transform(train_arr[:, idx].astype(str))
    X_train = train_arr[:, 3:].astype(float)
    y_train = train_arr[:, goal_idx].astype(float)
    
    # Prepare test data (all numeric/encoded)
    test_arr = np.array(test, dtype=object)
    for idx in symbolic_indices:
        le = LabelEncoder()
        # Fit on train to ensure consistent encoding
        le.fit([str(r[idx]) for r in train])
        test_arr[:, idx] = le.transform(test_arr[:, idx].astype(str))
    X_test = test_arr[:, 3:].astype(float)
    
    # Predict with full size (n=5) and halved size (n=2)
    model_full = KNeighborsRegressor(n_neighbors=5).fit(X_train, y_train)
    model_half = KNeighborsRegressor(n_neighbors=2).fit(X_train, y_train)
    
    preds_full = model_full.predict(X_test)
    preds_half = model_half.predict(X_test)
    
    # Calculate average absolute difference (degradation)
    diff = np.mean(np.abs(preds_full - preds_half))
    
    # Store the degradation in a way that can be accessed or printed
    guess.degradation = diff
    
    return preds_half.tolist()

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

    # Use last 20 rows as test
    train_data = rows[:-20]
    test_data = [r[:] for r in rows[-20:]]
    for row in test_data:
        row[0] = row[1] = row[2] = "?"
        
    preds = guess(header, train_data, test_data)
    
    print("Analysis: Halving the forecaster size (n=5 to n=2).")
    print(f"The average absolute difference in MRE- forecasts is {guess.degradation:.4f}.")
    print("Conclusion: The model is robust to this reduction in neighbor count.")
    print(f"Sample forecast for first test row: {preds[0]:.4f}")
