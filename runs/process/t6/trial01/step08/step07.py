import ezr
from math import exp, sqrt


def choose(header, rows, label):
    """Find the best setup within a budget of 50 labels."""
    # Identify goal columns: names ending in '-' (minimise) or '+' (maximise)
    goals = [(i, h.endswith('-')) for i, h in enumerate(header)
              if h.endswith('-') or h.endswith('+')]

    # Build a table from the rows we have so far.  We'll grow it as we label.
    tbl = ezr.Tbl(rows)

    # Train a tree on whatever we know; retrain after each new label.
    node = ezr.tree(tbl, tbl.rows)

    def predict_ydist(r):
        """Walk row to its leaf and return mean ydist of that leaf."""
        leaf_node = ezr.leaf(node, r)
        return leaf_node.mu

    # We'll keep track of the best labelled row seen so far.
    best_idx = None
    best_yd = 1e30

    budget = 50
    for _ in range(budget):
        if len(tbl.rows) >= budget:
            break

        # Label a new row (any unlabelled one; we pick the first).
        idx = next(i for i, r in enumerate(rows) if "?" not in str(r))
        lbl = label(idx)
        rows[idx] = lbl

        tbl = ezr.Tbl(rows)
        node = ezr.tree(tbl, tbl.rows)

        pred = predict_ydist(lbl)
        yd = ezr.ydist(tbl, lbl)

        if best_idx is None or yd < best_yd:
            best_idx = idx
            best_yd = yd

    return best_idx


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

    best = choose(header, rows, label)
    print(f"Best setup is row {best}.")
