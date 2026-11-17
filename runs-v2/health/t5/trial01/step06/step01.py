import ezr


def remember(header, rows):
    tbl = ezr.Tbl(rows)
    ranker_fn = ezr.ranker(tbl)
    wins_fn = ezr.wins(tbl)
    best = min(ranker_fn(r) for r in rows)
    avg  = sum(wins_fn(r) for r in rows) / len(rows)
    return [i for i, r in enumerate(rows) if ranker_fn(r) >= best - (avg - best) * 0.3]


if __name__ == "__main__":
    with open("Health-ClosedIssues0000.train.csv", encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]
    header = list(lines[0].split(","))
    rows   = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]
    positions = remember(header, rows)
    print(f"Top {len(positions)} of {len(rows)} rows:")
    for i in positions[:5]:
        print(f"  row {i}: {ezr.say([c for c in rows[i] if isinstance(c, float)], p=4)}")
