import ezr


def justify(header, rows, row):
    """Return (p, reason) for a row with ? goal cells."""
    tbl = ezr.Tbl(zip(header, rows))
    node = ezr.tree(tbl, tbl.rows)
    preds = [ezr.leaf(node, r).mu for r in rows]

    # Predict goals for the new row by filling ? with column means.
    filled = list(row)
    for c in tbl.x:
        if isinstance(c, ezr.Num):
            vals = [float(r[c.at]) for r in rows]
            mean_val = sum(vals) / len(vals)
            filled[c.at] = mean_val
        else:
            vals = [str(r[c.at]) for r in rows]
            most_common = max(set(vals), key=vals.count)
            filled[c.at] = most_common

    new_row = ezr.Tbl(zip(header, [filled]))
    new_node = ezr.tree(new_row, new_row.rows)
    new_pred = ezr.leaf(new_node, new_row.rows[0]).mu

    # Compare: how many existing rows has the new row beat?
    better = sum(1 for p in preds if new_pred < p)
    n = len(rows)
    p = better / n if n else 0.5

    reason = (f"The new row beats {p:.0%} of {n} existing rows "
              f"on goal closeness, with predicted ydist {new_pred:.4f}.")
    return (p, reason)


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "Health-ClosedIssues0000.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    # Use the last row (with ? goals) as the test row.
    test_row = rows[-1]
    p, reason = justify(header, rows[:-1], test_row)
    print(f"Result: {p:.2%} — {reason}")
