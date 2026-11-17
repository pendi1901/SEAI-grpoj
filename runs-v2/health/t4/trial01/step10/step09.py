import numpy as np
from step02 import guess


def spot(header, rows):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Use guess() to predict MRE- for each row based on its own features
    # Rows where prediction differs significantly from actual are suspicious
    
    feature_cols = [c for c in header if c not in goal_cols]
    
    def build_X(rows):
        X = np.zeros((len(rows), len(feature_cols)))
        for i, row in enumerate(rows):
            for j, col in enumerate(feature_cols):
                cell = row[header.index(col)]
                v = float(cell) if isinstance(cell, (int, float)) else 0.0
                X[i][j] = v
        return X
    
    train_X = build_X(rows)
    
    # Predict MRE- for each row using the same features
    preds = guess(header, rows, rows)[0:1]  # This won't work as-is since guess expects separate train/test
    
    # Actually, let me think differently. I need to predict each row's MRE- given its own inputs.
    # But guess() trains on all rows and predicts for test - that doesn't help directly.
    
    # Better approach: use the model from step02 but apply it per-row
    # Actually, let me just train a model once and predict
    
    y_train = np.array([float(row[header.index('MRE-')]) for row in rows])
    
    from sklearn.ensemble import RandomForestRegressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_X, y_train)
    
    suspicious = []
    for i, row in enumerate(rows):
        x_test = np.zeros((1, len(feature_cols)))
        for j, col in enumerate(feature_cols):
            cell = row[header.index(col)]
            v = float(cell) if isinstance(cell, (int, float)) else 0.0
            x_test[0][j] = v
        
        pred = model.predict(x_test)[0]
        
        actual_mre = y_train[i]
        diff = abs(pred - actual_mre)
        
        # If prediction is way off from reality, the row might be wrongly entered
        if diff > 0.1:  # threshold for suspiciousness
            suspicious.append(i)
    
    return sorted(suspicious, reverse=True)[:5]


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(map(float, row)) for _, row in df.iterrows()]

    suspicious = spot(header, rows)
    print(f"Suspicious rows: {suspicious}")
