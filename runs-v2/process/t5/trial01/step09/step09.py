#!/usr/bin/env python3 -B
"""step09.py: spot mistyped records."""


def spot(header, rows):
    """Return list of row indices with suspicious input values, most suspicious first."""
    # Identify pure-input numeric columns (uppercase start, not a goal)
    num_input = []  # column index
    for i, h in enumerate(header):
        if h[-1] == "-":
            continue
        if h[0].isupper():
            num_input.append(i)

    n = len(rows)
    stats = {}  # col_idx -> (median, q1, q3, iqr)
    for idx in num_input:
        vals = sorted(r[idx] for r in rows if isinstance(r[idx], float))
        if not vals:
            continue
        med = vals[n // 2]
        q1 = vals[n // 4]
        q3 = vals[3 * n // 4]
        iqr = q3 - q1
        stats[idx] = (med, q1, q3, iqr)

    suspicious = []
    for i, row in enumerate(rows):
        score = 0
        for idx in num_input:
            v = row[idx]
            if not isinstance(v, float):
                continue
            med, q1, q3, iqr = stats[idx]
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            if v < lower or v > upper:
                score += 1
        suspicious.append((score, i))

    suspicious.sort(reverse=True)
    return [i for _, i in suspicious]


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = [s for s in lines[0].split(",")]
    rows = [[__import__("ezr").atom(s) for s in line.split(",")] for line in lines[1:]]

    bad = spot(header, rows)
    print(f"Suspicious rows (most suspicious first): {bad}")
