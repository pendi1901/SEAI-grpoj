#!/usr/bin/env python3 -B
"""step04.py: approve proposals one at a time."""
import ezr


def flow(header, row, seen):
    """Approve the current proposal if it is good enough.

    Returns True to choose and stop; False otherwise.
    """
    # Need at least 3 rows to build a meaningful model
    if len(seen) < 3:
        return False

    tbl = ezr.Tbl(zip(header, seen))
    ranker_fn = ezr.ranker(tbl)

    predicted_ydist = ranker_fn(row)
    best_seen = min(ezr.ydist(tbl, r) for r in seen)

    # Approve if at least 5% better than the best seen so far
    return predicted_ydist <= best_seen * 0.95


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]

    header = [s for s in lines[0].split(",")]
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    approved_idx = None
    seen = []

    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Approved proposal {i + 1}")
            approved_idx = i
            break
        seen.append(row)

    if approved_idx is not None:
        print(f"Chose row {approved_idx + 1} out of {len(rows)}")
    else:
        print("No proposals approved")
