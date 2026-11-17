import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def remember(header, rows):
    # Identify goal columns (end with '-' or '+')
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Find best values per goal column across all valid rows
    min_vals = {}
    max_vals = {}
    for col in goal_cols:
        vals = []
        for row in rows:
            cell = row[header.index(col)]
            if cell == "?" or (isinstance(cell, float) and np.isnan(cell)):
                continue
            v = float(cell)
            vals.append(v)
        
        if '-' in col:
            min_vals[col] = min(vals) if vals else 0.0
        else:
            max_vals[col] = max(vals) if vals else 0.0
    
    # Score each row: sum of absolute deviations from best on goals
    scores = []
    for i, row in enumerate(rows):
        s = 0.0
        valid = True
        for col in goal_cols:
            cell = row[header.index(col)]
            if cell == "?" or (isinstance(cell, float) and np.isnan(cell)):
                continue
            v = float(cell)
            if '-' in col:
                s += abs(v - min_vals[col])
            else:
                s += abs(v - max_vals[col])
        scores.append(s)
    
    # Return positions of top rows (at least 1, at most 5%)
    n = len(rows)
    k = max(1, int(n * 0.05))
    sorted_indices = np.argsort(scores)[:k]
    return sorted_indices.tolist()


def guess(header, train, test):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    target_col = goal_cols[0]  # first goal column to predict
    
    feature_cols = [c for c in header if c not in goal_cols]
    
    def build_X(rows):
        X = np.zeros((len(rows), len(feature_cols)))
        for i, row in enumerate(rows):
            for j, col in enumerate(feature_cols):
                cell = row[header.index(col)]
                v = float(cell) if isinstance(cell, (int, float)) else 0.0
                X[i][j] = v
        return X
    
    train_X = build_X(train)
    test_X = build_X(test)
    
    y_train = np.array([float(row[header.index(target_col)]) for row in train])
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_X, y_train)
    
    return model.predict(test_X).tolist()


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(map(float, row)) for _, row in df.iterrows()]
    
    best_positions = remember(header, rows)
    print(f"Best {len(best_positions)} out of {len(rows)} setups:")
    for pos in best_positions:
        print(f"  Row {pos}: MRE={df.iloc[pos]['MRE-']:.4f}, ACC={df.iloc[pos]['ACC+']:.4f}, PRED40={df.iloc[pos]['PRED40+']:.4f}")

    preds = guess(header, rows, [])
    print(f"\nPredicted MRE for {len(preds)} test configurations:")
    for i, p in enumerate(preds):
        print(f"  Config {i}: estimated MRE={p:.4f}")
