def remember(header, rows):
    goals_min = [c for c in header if c.endswith('-')]
    goals_max = [c for c in header if c.endswith('+')]

    scored = []
    for i, row in enumerate(rows):
        if row[header.index('attrition')] == 'No':
            score = sum(row[c] for c in goals_min) + sum(-row[c] for c in goals_max)
            scored.append((score, i))

    scored.sort(reverse=True)
    max_count = int(len(rows) * 0.05)
    best_positions = [pos for _, pos in scored[:max_count]]
    return best_positions


if __name__ == "__main__":
    import csv

    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    positions = remember(header, rows)
    print(f"Best {len(positions)} of 1470 stayers (by goal alignment):")
    for p in positions:
        print(f"  row {p}")
