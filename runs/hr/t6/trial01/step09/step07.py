import ezr
from step01 import remember


def choose(header, rows, label):
    """Pick the best row from at most 50 labelled ones."""
    tbl = ezr.Tbl(iter([header] + rows))

    # Start with a few random labels to get initial centroids
    start = min(4, len(rows))
    init_rows = [label(i) for i in range(start)]
    both = ezr.clone(tbl, init_rows)

    # Budget: 50 labels total
    cap = 50
    todo = list(range(len(rows)))

    while todo and len(both.rows) < cap:
        cb, cr = ezr.mids(best:=ezr.clone(tbl, both.rows[:int(ezr.sqrt(start))])), \
                  ezr.mids(rest:=ezr.clone(tbl, both.rows[int(ezr.sqrt(start)):])))

        # Sort unlabelled rows by closeness to best centroid minus rest centroid
        todo.sort(key=lambda z: ezr.xdist(tbl, rows[z], cr) - ezr.xdist(tbl, rows[z], cb))

        i = todo.pop(0)
        lab = label(i)
        both.rows.append(lab)
        # Keep best half small; move rest to the other side
        if len(best.rows) > int(ezr.sqrt(len(both.rows))):
            rest.rows.append(ezr.addCols(best, best.rows.pop(), -1))

    # Sort by ydist and return index of the best row
    both.rows.sort(key=lambda r: ezr.ydist(tbl, r))
    return both.rows[0].at


if __name__ == "__main__":
    import csv
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    best_idx = choose(header, rows, label)
    print(f"Best row index: {best_idx}")
