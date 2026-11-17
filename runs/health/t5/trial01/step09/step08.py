import ezr


def fix(header, row, levers):
    """Pick the best allowed value for each lever that minimises ydist."""
    tbl = ezr.Tbl(zip(header, [row]))
    goals = [c for c in tbl.y if c.goal != 0]

    # For each lever, try every allowed value and keep the one giving lowest ydist.
    best = {}
    cur_y = ezr.ydist(tbl, row)
    for col_name, vals in levers.items():
        at = header.index(col_name)
        best_val = row[at]
        best_y = cur_y
        for v in vals:
            trial = list(row)
            trial[at] = v
            y = ezr.ydist(tbl, trial)
            if y < best_y:
                best_y = y
                best_val = v
        best[col_name] = best_val

    return best


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "Health-ClosedIssues0000.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    # Use the last row (the bad one with ? goals).
    bad_row = rows[-1]
    levers = {
        "N_estimators": [5, 20],
        "criterion": ["squared_error", "absolute_error"],
        "Max_depth": [8, 14],
    }

    fix_map = fix(header, bad_row, levers)
    print(f"Recommended changes: {fix_map}")
