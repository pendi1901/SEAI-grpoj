import numpy as np
from step01 import remember


def blame(header, rows):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]

    # Score each row: sum of absolute deviations from best on goals
    scores = []
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

    for i, row in enumerate(rows):
        s = 0.0
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

    # Worst rows (highest score = furthest from best performance)
    worst_indices = np.argsort(scores)[::-1][:max(1, int(len(rows) * 0.2))]
    worst_set = set(worst_indices.tolist())

    # Input columns (not goals)
    input_cols = [c for c in header if c not in goal_cols]

    # For each input col: compare average value in worst vs best rows
    explanations = []
    for col in input_cols:
        vals_worst = []
        vals_best = []
        for i, row in enumerate(rows):
            cell = row[header.index(col)]
            if isinstance(cell, (int, float)):
                v = float(cell)
                if i in worst_set:
                    vals_worst.append(v)
                elif scores[i] <= np.percentile(scores, 20):
                    vals_best.append(v)

        if vals_worst and vals_best:
            avg_worst = sum(vals_worst) / len(vals_worst)
            avg_best = sum(vals_best) / len(vals_best)
            diff = abs(avg_worst - avg_best)
            explanations.append((col, diff))

    # Sort by magnitude of difference (most explanatory first)
    explanations.sort(key=lambda x: -x[1])

    return [c for c, _ in explanations[:5]]


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(map(float, row)) for _, row in df.iterrows()]

    bad_cols = blame(header, rows)
    print(f"Bad setups are most damaged by: {', '.join(bad_cols)}")
