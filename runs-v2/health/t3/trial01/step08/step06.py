import numpy as np
from sklearn.linear_model import LinearRegression


def justify(header, rows, row):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if not c.endswith('-') and not c.endswith('+')]

    # Build training data from the complete rows (which have real goals)
    X_train = np.array([[float(row[input_cols.index(c)]) for c in input_cols] for row in rows])

    # Train a separate model per goal column to predict what the test row's goals would be
    models = {}
    for col in goal_cols:
        y_col = [float(r[header.index(col)]) for r in rows]
        m = LinearRegression()
        m.fit(X_train, np.array(y_col))
        models[col] = m

    # Predict the hidden goals of the test row
    x_test = [float(row[input_cols.index(c)]) for c in input_cols]
    predicted_goals = {col: float(models[col].predict([x_test])[0]) for col in goal_cols}

    # Compute best / worst per goal across all training rows (for normalisation)
    best = {}
    worst = {}
    for col in goal_cols:
        vals = [float(r[header.index(col)]) for r in rows]
        if col.endswith('-'):
            best[col], worst[col] = min(vals), max(vals)
        else:
            best[col], worst[col] = max(vals), min(vals)

    # Score a row by summing normalised goal values (0.5 when span is zero)
    def score(goals):
        s = 0.0
        for col in goal_cols:
            v = goals[col]
            span = best[col] - worst[col]
            if span > 1e-9:
                normed = (v - worst[col]) / span
            else:
                normed = 0.5
            s += normed
        return s

    # Score each training row and the test row
    train_scores = [score({col: float(r[header.index(col)]) for col in goal_cols}) for r in rows]
    test_score = score(predicted_goals)

    # Fraction of training rows that are worse than the test row
    n_better = sum(1 for s in train_scores if s < test_score)
    p = n_better / len(rows)

    reason = f"This setup beats {p:.0%} of all other setups."
    return (p, reason)


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(r) for r in df.values]

    # Use the first row (with real goals) to demonstrate; replace goal cells with "?"
    demo_row = list(rows[0])
    for i, col in enumerate(header):
        if col.endswith('-') or col.endswith('+'):
            demo_row[i] = "?"

    p, reason = justify(header, rows, demo_row)
    print(f"{reason}")
