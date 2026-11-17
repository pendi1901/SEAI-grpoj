import ezr

def remember(header, rows):
    tbl = ezr.Tbl([header] + rows)
    scored = [(ezr.ydist(tbl, r), i) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: x[0])
    n = max(1, int(len(scored) * 0.05))
    return [i for _, i in scored[:n]]

if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "Health-ClosedIssues0000.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        rows.append([ezr.atom(s) for s in line.split(",")])

    positions = remember(header, rows)
    print(f"Top {len(positions)} trustworthy setups:")
    for p in positions[:5]:
        print(f"  Row {p}")
