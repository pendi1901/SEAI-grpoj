import ezr
from math import exp, sqrt


def flow(header, row, seen):
    """Approve or reject a proposal that just arrived."""
    train = list(seen)

    if len(train) < 3:
        return True

    tbl = ezr.Tbl(train)
    node = ezr.tree(tbl, tbl.rows)

    def predict_ydist(r):
        leaf_node = ezr.leaf(node, r)
        return leaf_node.mu

    pred = predict_ydist(row)
    train_ydists = [ezr.ydist(tbl, r) for r in train]
    best_train = min(train_ydists) if train_ydists else 1.0

    return pred <= best_train * 2.0


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "pom3a.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")

    rows = []
    for line in lines[1:]:
        cells = line.split(",")
        row = []
        for c in cells:
            s = c.strip()
            try: row.append(float(s))
            except ValueError:
                if s.lower() == "true":  row.append(True)
                elif s.lower() == "false": row.append(False)
                else:                   row.append(s)
        rows.append(row)

    approved = []
    for i, r in enumerate(rows):
        seen = rows[:i] if i > 0 else []
        approve = flow(header, r, seen)
        if approve:
            approved.append(i)

    print(f"Approved {len(approved)} of {len(rows)} proposals (rows {approved}).")
