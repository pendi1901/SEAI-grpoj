import ezr


def flow(header, row, seen):
    """Return True when we have enough rows to ship; False otherwise."""
    tbl = ezr.Tbl(zip(header, seen + [row]))
    goals = [c for c in tbl.y if c.goal != 0]
    ys = [(ezr.ydist(tbl, r), i) for i, r in enumerate(seen + [row])]
    ys.sort()
    n = len(ys)
    avg_y = sum(y for y, _ in ys) / n
    lo_y = ys[0][0]
    threshold = (avg_y + lo_y) / 2
    candidates = [i for i, y in zip(*zip(*ys), range(n)) if y < threshold]
    if not candidates:
        idx = max(1, int(0.05 * n))
        return False
    limit = max(1, int(0.05 * n))
    best = sorted(candidates)[:limit]
    return len(best) >= 1


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "Health-ClosedIssues0000.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]

    tbl = ezr.Tbl(zip(header, rows))
    goals = [c for c in tbl.y if c.goal != 0]
    ys = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows)]
    ys.sort()
    n = len(ys)
    avg_y = sum(y for y, _ in ys) / n
    lo_y = ys[0][0]
    threshold = (avg_y + lo_y) / 2
    candidates = [i for i, y in zip(*zip(*ys), range(n)) if y < threshold]
    limit = max(1, int(0.05 * n))
    best = sorted(candidates)[:limit]

    print(f"Rows shipped: {len(best)} / {n}")
    print(f"Best ydist: {best[0]:.4f} (threshold {threshold:.4f})")
