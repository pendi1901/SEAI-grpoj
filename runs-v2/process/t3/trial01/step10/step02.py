import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def guess(header, train, test):
    df = pd.DataFrame(train, columns=header)

    goal_cols = [h for h in header if h.endswith('-')]
    input_cols = [h for h in header if not h.endswith('-')]

    for col in goal_cols:
        df[col] = df[col].replace('?', np.nan).astype(float)

    models = {}
    for col in goal_cols:
        X = df[input_cols].values
        y = df[col].dropna().values
        mask = ~df[col].isna()
        if len(y) > 0:
            model = LinearRegression()
            model.fit(X[mask], y)
            models[col] = model

    results = []
    for row in test:
        X_pred = np.array([row[c] for c in input_cols])
        pred = models['Cost-'].predict(X_pred)[0]
        results.append(float(pred))

    return results


if __name__ == "__main__":
    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    result = guess(header, rows, [])
    print(f"Predicted Cost- values (first 5): {result[:5]}")
