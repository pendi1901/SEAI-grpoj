import pandas as pd
import numpy as np


def guess(header, train, test):
    # Identify goal columns (end with '-') and input columns
    goal_cols = [c for c in header if c.endswith('-')]
    input_cols = [c for c in header if not c.endswith('-')]

    X_train = np.array([[float(cell) for cell in row] for row in train])
    y_train = np.array([float(row[0]) for row in train])  # first goal column: Cost-

    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X_train, y_train)

    X_test = np.array([[float(cell) for cell in row] for row in test])
    preds = model.predict(X_test).tolist()
    return preds


if __name__ == "__main__":
    df = pd.read_csv("pom3a.train.csv")
    header = list(df.columns)
    rows = [list(row) for _, row in df.iterrows()]

    test_rows = []
    for _, r in df.iterrows():
        new_row = []
        for c in header:
            if c.endswith('-'):
                new_row.append('?')
            else:
                new_row.append(float(r[c]))
        test_rows.append(new_row)

    preds = guess(header, rows, test_rows)
    print(f"Predicted Cost- for {len(preds)} setups:")
    for p in preds[:5]:
        print(f"  {p:.4f}")
