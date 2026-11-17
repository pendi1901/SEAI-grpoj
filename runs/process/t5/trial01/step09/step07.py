#!/usr/bin/env python3 -B
"""step07.py: pick the best of up to 50 setups by labelling them."""
import ezr


def choose(header, rows, label):
    """Return the index (int) of the best row among those we can afford to trial.

    Every goal cell in `rows` is "?".  Calling label(i) returns the list of true
    goal values for rows[i]; we may call it at most 50 times.  We return the
    position of the best row found.
    """
    # Build a table from the full (unlabelled) data so that ydist works on
    # rows whose goals are still "?".
    tbl = ezr.Tbl([header] + rows)

    # Acquire labels for up to 50 rows, starting with a few random ones.
    cap = 50
    labelled_rows = ezr.acquire(tbl, cap=cap, label=label)

    # For each labelled row we know the true goal values; compute its real ydist.
    scored = []
    for i, r in enumerate(labelled_rows):
        # Reconstruct a full row with goals filled in from the oracle.
        full_row = list(r)
        for j, col_name in enumerate(header):
            if col_name[-1] in "+-":
                full_row[j] = r[j]  # already labelled

        yd = ezr.ydist(tbl, full_row)
        scored.append((yd, i))

    scored.sort(key=lambda x: x[0])
    return scored[0][1]


if __name__ == "__main__":
    import os

    path = os.path.join(os.path.dirname(__file__), "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]

    header = lines[0].split(",")
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    def label(i):
        return [float(rows[i][j]) for j, name in enumerate(header)
                if name[-1] in "+-"]

    best_idx = choose(header, rows, label)
    print(f"Best setup: row {best_idx}")
