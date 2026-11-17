import sys
sys.path.insert(0, '.')
from step01 import remember


def blame(header, rows):
    goals = [h for h in header if h.endswith('-') or h.endswith('+')]
    n = len(rows)

    # Score every row with the same normalisation as remember().
    scores = np.zeros(n)
    for col in goals:
        vals = []
        for row in rows:
            v = float(row[header.index(col)])
            vals.append(v)
        arr = np.array(vals)
        if arr.max() == arr.min():
            scores += 0.5
        else:
            normed = (arr - arr.min()) / (arr.max() - arr.min())
            if col.endswith('-'):
                scores += (1.0 - normed)
            else:
                scores += normed

    sorted_indices = np.argsort(scores)[::-1]
    top_k = max(1, int(n * 0.05))
    good_set = set(sorted_indices[:top_k].tolist())
    bad_set = set(sorted_indices[-top_k:].tolist())

    input_cols = [c for c in header if not c.endswith('-') and not c.endswith('+')]

    blame_vals = []
    for col in input_cols:
        good_vals = []
        bad_vals = []
        for i, row in enumerate(rows):
            v = float(row[header.index(col)])
            if i in good_set:
                good_vals.append(v)
            elif i in bad_set:
                bad_vals.append(v)

        if not good_vals or not bad_vals:
            blame_vals.append((0.0, col))
            continue

        g_mean = np.mean(good_vals)
        b_mean = np.mean(bad_vals)
        diff = abs(g_mean - b_mean)

        all_vals = [float(row[header.index(col)]) for row in rows]
        arr_all = np.array(all_vals)
        col_range = float(arr_all.max() - arr_all.min()) if len(all_vals) > 1 else 1.0
        norm_diff = diff / col_range if col_range > 0 else 0.0

        blame_vals.append((norm_diff, col))

    blame_vals.sort(key=lambda x: -x[0])
    return [col for _, col in blame_vals[:3]]


if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    bad_cols = blame(header, rows)
    print(f"Blame: {bad_cols}")
