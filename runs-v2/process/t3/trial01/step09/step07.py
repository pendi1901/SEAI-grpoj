import pandas as pd
import numpy as np


def choose(header, rows, label):
    goal_cols = [h for h in header if h.endswith('-')]

    n_try = min(50, len(rows))

    best_idx = None
    best_score = -np.inf

    for i in range(n_try):
        goals = label(i)

        scores = {}
        for col in goal_cols:
            val = goals[col] if col in goals else '?'
            if isinstance(val, (int, float)):
                scores[col] = float(val)
            else:
                scores[col] = 0.0

        avg_score = np.mean(list(scores.values())) if len(scores) > 0 else -np.inf

        if avg_score > best_score:
            best_score = avg_score
            best_idx = i

    return best_idx


if __name__ == "__main__":
    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    goal_cols = [h for h in header if h.endswith('-')]
    for col in goal_cols:
        for i, row in enumerate(rows):
            if pd.notna(df.iloc[i][col]):
                rows[i][header.index(col)] = '?'

    result = choose(header, rows, lambda i: [df.iloc[i][c] for c in goal_cols])
    print(f"Best setup is at position {result}")
