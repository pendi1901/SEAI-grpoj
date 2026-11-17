#!/usr/bin/env python3 -B
"""step01.py: find setups unusually well on all three bills."""
import ezr


def remember(header, rows):
    """Return positions of best rows (at least 1, at most 5%)."""
    tbl = ezr.Tbl([header] + rows)
    score_fn = ezr.wins(tbl)
    scored = [(score_fn(r), i) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: -x[0])
    n = max(1, len(scored) // 20)
    return [i for _, i in scored[:n]]


if __name__ == "__main__":
    import os

    path = os.path.join(os.path.dirname(__file__), "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]
    positions = remember(header, rows)
    print(f"Top {len(positions)} of {len(rows)} setups:")
    for p in positions:
        print(f"  Row {p}")
