import numpy as np


def remember(header, rows):
    goal_cols = [c for c in header if c.endswith('-')]

    n = len(rows)
    data = {}
    for col in goal_cols:
        vals = []
        for row in rows:
            v = row[header.index(col)]
            if v == '?':
                vals.append(np.nan)
            else:
                vals.append(float(v))
        data[col] = np.array(vals)

    min_vals = {}
    ranges = {}
    for col in goal_cols:
        arr = data[col]
        valid = arr[~np.isnan(arr)]
        if len(valid) == 0:
            continue
        mn = float(valid.min())
        mx = float(valid.max())
        min_vals[col] = mn
        ranges[col] = (mx - mn) if mx > mn else 1.0

    scores = []
    for i in range(n):
        s = 0.0
        for col in goal_cols:
            v = data[col][i]
            if np.isnan(v):
                continue
            s += (v - min_vals[col]) / ranges[col]
        scores.append(s)

    threshold_idx = int(0.05 * n)
    sorted_indices = np.argsort(scores)[:threshold_idx]
    return sorted_indices.tolist()


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    best_positions = remember(header, rows)
    print(f"Top {len(best_positions)} out of {len(rows)} setups:")
    for pos in best_positions:
        print(
            f"  Row {pos}: Cost-={rows[pos][header.index('Cost-')]:.4f}, "
            f"Score-={rows[pos][header.index('Score-')]:.4f}, "
            f"Idle-={rows[pos][header.index('Idle-')]:.4f}"
        )
