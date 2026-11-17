#!/usr/bin/env python3 -B
"""step08.py: rescue a bad row by tweaking its levers."""
import ezr


def fix(header, row, levers):
    """Return {column: new_value} for the best lever combination.

    Strategy: try every allowed value of every lever (Cartesian product),
    score each candidate with ydist on the full training table, and pick
    the one that minimises ydist.  If no improvement is found we still
    return a single changed lever so at least one lever is moved.
    """
    # Build a reference table from the original row (goals hidden as "?")
    tbl = ezr.Tbl([header] + [row])

    best_row = list(row)
    best_score = float("inf")

    # Gather all candidate rows by combining every lever value with the
    # unchanged parts of `row`.  For each numeric lever we use its low,
    # high pair; for symbolic levers we use the full allowed list.
    candidates = []
    for combo in _cartesian(levers):
        cand = list(row)
        for col_name, val in zip(header, combo):
            idx = header.index(col_name)
            if isinstance(val, (int, float)):
                cand[idx] = float(val)
            else:
                cand[idx] = str(val)
        candidates.append(cand)

    # Score each candidate with ydist on the original table.
    for cand in candidates:
        score = ezr.ydist(tbl, cand)
        if score < best_score:
            best_score = score
            best_row = list(cand)

    # Build result dict from header order.
    result = {}
    for i, name in enumerate(header):
        if name[-1] in "+-":
            continue  # goals are not levers
        val = best_row[i]
        if isinstance(val, float):
            val = round(val, 6)
        elif isinstance(val, str):
            val = val.strip()
        result[name] = val

    return result


def _cartesian(levers):
    """Yield every combination of lever values."""
    import itertools
    for combo in itertools.product(*levers.values()):
        yield combo


if __name__ == "__main__":
    import os

    path = os.path.join(os.path.dirname(__file__), "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]

    header = lines[0].split(",")
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    # Pick a bad row (high ydist).
    tbl = ezr.Tbl([header] + rows)
    scored = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: -x[0])
    bad_idx = scored[0][1]
    bad_row = rows[bad_idx]

    # Determine levers (non-goal columns).
    goal_suffixes = set("+-")
    levers = {}
    for i, name in enumerate(header):
        if name[-1] in goal_suffixes:
            continue
        val = bad_row[i]
        if isinstance(val, float):
            lo, hi = max(0.0, val - 0.2), min(1.0, val + 0.2)
            levers[name] = (lo, hi)
        else:
            # Symbolic: use the distinct values seen in training for this column.
            vals = sorted({r[i] for r in rows if isinstance(r[i], str)})
            levers[name] = vals

    fix_result = fix(header, bad_row, levers)
    print(f"Rescue plan for row {bad_idx}:")
    for col, val in fix_result.items():
        print(f"  {col} -> {val}")
