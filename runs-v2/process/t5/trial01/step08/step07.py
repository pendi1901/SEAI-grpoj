#!/usr/bin/env python3 -B
"""step07.py: pick the best of up to 50 trial setups."""
import ezr


def choose(header, rows, label):
    """Return index (0-based) of the best row found within the budget.

    Every goal cell in `rows` is "?".  Calling label(i) returns the list of
    true goal values for rows[i]; you may call it at most 50 times.
    Lower ydist = better, so we pick the smallest ydist seen.
    """
    # Build a table from the fully-hidden rows (goals are "?", inputs real).
    tbl = ezr.Tbl(zip(header, rows))

    best_idx = None
    best_y = 1e30

    for i in range(len(rows)):
        # Fill goals with column means so we can score.
        row = list(rows[i])
        for j, col_name in enumerate(header):
            if col_name.endswith("-") and row[j] == "?":
                col_obj = tbl.cols[j]
                if hasattr(col_obj, "mu"):
                    row[j] = col_obj.mu

        # Score via the ranker (tree on all rows).
        score = ezr.ranker(tbl)(row)
        if score < best_y:
            best_y = score
            best_idx = i

    return best_idx


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]

    header = [s for s in lines[0].split(",")]
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    # Mask goal cells with "?" so the function sees hidden data.
    for row in rows:
        for j, col_name in enumerate(header):
            if col_name.endswith("-") and row[j] != "?":
                row[j] = "?"

    idx = choose(header, rows, label)

    # Reveal the chosen row's goals to print a readable answer.
    tbl = ezr.Tbl(zip(header, rows))
    picked = list(rows[idx])
    for j, col_name in enumerate(header):
        if col_name.endswith("-"):
            col_obj = tbl.cols[j]
            if hasattr(col_obj, "mu"):
                picked[j] = col_obj.mu

    print(f"Best setup: row {idx + 1} (of {len(rows)}).")
