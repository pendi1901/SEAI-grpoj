import csv
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from step02 import guess as original_guess

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows using a K-Nearest Neighbors
    regressor. To simulate 'halving the size of the forecaster', we reduce the 
    number of neighbors (k) used in the model.
    """
    # Identify input columns (all except goals)
    input_indices = [i for i, col in enumerate(header) if not (col.endswith('-') or col.endswith('+'))]
    
    def prepare_data(data_rows):
        X = []
        for row in data_rows:
            features = []
            for i in input_indices:
                val = row[i]
                if isinstance(val, str):
                    val = hash(val) % 100
                features.append(float(val))
            X.append(features)
        return np.array(X)

    X_train = prepare_data(train)
    y_train = np.array([row[0] for row in train])
    X_test = prepare_data(test)
    
    # Original used 5 neighbors. Halving the 'size' of the forecaster 
    # (in terms of local neighborhood complexity) to 2.
    model = KNeighborsRegressor(n_neighbors=2)
    model.fit(X_train, y_train)
    
    return model.predict(X_test).tolist()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    # Compare original (step02) vs halved (step12)
    train_data = rows[:-10]
    test_data = [[r[i] if i in [3, 4, 5, 6, 7] else "?" for i in range(len(header))] for r in rows[-10:]]
    actuals = [r[0] for r in rows[-10:]]
    
    preds_orig = original_guess(header, train_data, test_data)
    preds_halved = guess(header, train_data, test_data)
    
    err_orig = np.mean([abs(p - a) for p, a in zip(preds_orig, actuals)])
    err_halved = np.mean([abs(p - a) for p, a in zip(preds_halved, actuals)])
    
    print("Impact of halving forecaster size (reducing neighbors from 5 to 2):")
    print(f"Original Mean Absolute Error: {err_orig:.4f}")
    print(f"Halved Size Mean Absolute Error: {err_halved:.4f}")
    print(f"Performance degradation: {((err_halved - err_orig) / err_orig) * 100:.2f}% increase in error.")
