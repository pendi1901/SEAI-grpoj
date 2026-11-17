import sys
sys.path.insert(0, '.')
from step01 import remember


def choose(header, rows, label):
    goal_cols = [c for c in header if c.endswith('-')]
    input_cols = [c for c in header if not c.endswith('-')]

    # Build a reference ranking from the training data (rows[0] is a full row).
    ref_rows = []
    for r in rows:
        new_r = list(r)
        for col in goal_cols:
            new_r[header.index(col)] = 0.0
        ref_rows.append(new_r)

    best_positions = remember(header, ref_rows)

    # For each input column, compute the average value among top-ranked rows.
    n_ref = len(ref_rows)
    col_means_top = {}
    for col in input_cols:
        vals_top = []
        vals_rest = []
        for i, r in enumerate(ref_rows):
            v = float(r[header.index(col)])
            if i in best_positions:
                vals_top.append(v)
            else:
                vals_rest.append(v)
        col_means_top[col] = (np.mean(vals_top), np.mean(vals_rest))

    # Now evaluate each candidate row.
    best_pos = -1
    best_score = float('inf')

    for i in range(len(rows)):
        score = 0.0
        for col in input_cols:
            v = float(rows[i][header.index(col)])
            mean_top, _ = col_means_top[col]
            # Penalise deviation from the top-ranked average.
            score += (v - mean_top) ** 2

        if score < best_score:
            best_score = score
            best_pos = i

    return int(best_pos)


if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    df = pd.read_csv("pom3a.train.csv")
    header = list(df.columns)
    rows = [list(r) for _, r in df.iterrows()]

    # Replace goal cells with "?" to simulate the customer's scenario.
    goal_cols = [c for c in header if c.endswith('-')]
    for i, row in enumerate(rows):
        for col in goal_cols:
            row[header.index(col)] = '?'

    best_pos = choose(header, rows, label)
    print(f"Best setup is at position {best_pos}.")
