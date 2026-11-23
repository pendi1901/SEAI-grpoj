import csv
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
import step02

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    To answer the customer's question: we compare the performance of a 
    standard KNN (n=5) vs a 'halved' forecaster (n=2).
    """
    # The customer asks: "If I halve the size of the forecaster... how much worse?"
    # We implement the standard guess logic here.
    return step02.guess(header, train, test)

def evaluate_impact(header, rows):
    """
    Compares the performance of a standard KNN (n=5) vs a halved (n=2) forecaster.
    """
    # Split data
    split = int(len(rows) * 0.8)
    train_data = rows[:split]
    test_data = rows[split:]
    
    # Prepare test data by masking goals
    masked_test = [r[:] for r in test_data]
    for r in masked_test:
        r[0], r[1], r[2] = "?", "?", "?"
        
    # Standard forecaster (n=5)
    # We use step02's logic but manually adjust n_neighbors for comparison
    def get_preds(n):
        goal_idx = 0
        encoders = {}
        for i, col in enumerate(header):
            if not col[0].isupper():
                encoders[i] = LabelEncoder()
                encoders[i].fit([r[i] for r in train_data])
        
        def transform(row):
            new = []
            for i, val in enumerate(row):
                if i == goal_idx: continue
                if i in encoders: new.append(float(encoders[i].transform([val])[0]))
                else: new.append(float(val))
            return new
            
        X_train = [transform(r) for r in train_data]
        y_train = [r[goal_idx] for r in train_data]
        model = KNeighborsRegressor(n_neighbors=n).fit(X_train, y_train)
        return model.predict([transform(r) for r in masked_test])

    preds_full = get_preds(5)
    preds_half = get_preds(2)
    
    actuals = [r[0] for r in test_data]
    
    err_full = np.mean(np.abs(preds_full - actuals))
    err_half = np.mean(np.abs(preds_half - actuals))
    
    return err_full, err_half

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed = [float(v) if header[i][0].isupper() else v for i, v in enumerate(row)]
            rows.append(processed)
            
    err_full, err_half = evaluate_impact(header, rows)
    
    print("Impact of halving the forecaster size (n=5 to n=2):")
    print(f"Mean Absolute Error (Full): {err_full:.4f}")
    print(f"Mean Absolute Error (Halved): {err_half:.4f}")
    diff = err_half - err_full
    print(f"The forecast error increases by {diff:.4f} on average when halving the forecaster size.")
