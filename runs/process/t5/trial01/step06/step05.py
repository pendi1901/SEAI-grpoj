#!/usr/bin/env python3 -B
"""step05.py: blame the features that make setups bad."""
import ezr


def blame(header, rows):
    """Return names of input columns (not goals) that explain why worst rows are bad.

    Worst = highest ydist. We compare feature values in worst vs best rows.
    """
    tbl = ezr.Tbl([header] + rows)
    ranker_fn = ezr.ranker(tbl)

    # Score all rows by predicted ydist
    scored = [(ranker_fn(r), i, r) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: -x[0])  # worst first

    n_worst = max(1, len(scored) // 20)
    n_best = max(1, len(scored) // 5)

    worst_rows = [s[2] for s in scored[:n_worst]]
    best_rows = [s[2] for s in scored[-n_best:]]

    # For each non-goal column, check if worst rows have worse values
    blame_scores = []
    goal_suffixes = set("+-")

    for i, col_name in enumerate(header):
        if col_name[-1] in goal_suffixes:
            continue

        worst_vals = [float(r[i]) for r in worst_rows if isinstance(r[i], (int, float))]
        best_vals = [float(r[i]) for r in best_rows if isinstance(r[i], (int, float))]

        if not worst_vals or not best_vals:
            continue

        mean_worst = sum(worst_vals) / len(worst_vals)
        mean_best = sum(best_vals) / len(best_vals)

        # Higher difference means this feature distinguishes bad from good setups
        diff = abs(mean_worst - mean_best)
        blame_scores.append((diff, col_name))

    # Sort by magnitude of difference (most explanatory first)
    blame_scores.sort(key=lambda x: -x[0])

    return [name for _, name in blame_scores[:5]]


if __name__ == "__main__":
    import os

    path = os.path.join(os.path.dirname(__file__), "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]

    header = lines[0].split(",")
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    result = blame(header, rows)
    print(f"Blame: {', '.join(result)}")
