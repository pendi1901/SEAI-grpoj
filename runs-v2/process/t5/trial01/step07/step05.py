#!/usr/bin/env python3 -B
"""step05.py: why do our worst setups leave people waiting?"""
import ezr


def blame(header, rows):
    """Return names of input columns that best explain the worst rows."""
    tbl = ezr.Tbl(zip(header, rows))

    # Score every row with ydist (lower is better)
    scored = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows)]
    scored.sort()

    n = len(scored)
    worst = [rows[i] for _, i in scored[:n // 4]]
    best = [rows[i] for _, i in scored[-n // 4:]]

    # For each numeric input column, compare mean between worst and best
    out = []
    for col in tbl.x:
        if type(col) is ezr.Sym:
            continue
        wv = [r[col.at] for r in worst if r[col.at] != "?"]
        bv = [r[col.at] for r in best if r[col.at] != "?"]
        if not wv or not bv:
            continue
        wm, wn = sum(wv) / len(wv), len(wv)
        bm, bn = sum(bv) / len(bv), len(bv)
        # Effect size: how many pooled SDs apart?
        pool = ((wn - 1) * ezr.div(col) ** 2 + (bn - 1) * ezr.div(col) ** 2) / max(1, wn + bn - 2)
        if pool > 0:
            diff = abs(wm - bm) / (ezr.sqrt(pool))
            # Columns that differ by more than ~0.5 SD are worth mentioning
            if diff >= 0.5:
                out.append(col.txt)

    return out


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = [s for s in lines[0].split(",")]
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    bad_cols = blame(header, rows)
    print(f"Worst setups differ from best in: {', '.join(bad_cols)}")
