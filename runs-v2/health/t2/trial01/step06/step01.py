def _to_float(cell):
    try:
        return float(cell)
    except (ValueError, TypeError):
        return 0.0


def remember(header, rows):
    minimise = [c for c in header if c.endswith('-')]
    maximise = [c for c in header if c.endswith('+')]

    n_rows = len(rows)
    max_return = max(1, int(n_rows * 0.05))

    scored = []
    for i, row in enumerate(rows):
        score = 0.0
        for col in minimise:
            v = _to_float(row[header.index(col)])
            score += v
        for col in maximise:
            v = _to_float(row[header.index(col)])
            score -= v
        scored.append((score, i))

    scored.sort()
    return [pos for _, pos in scored[:max_return]]


if __name__ == "__main__":
    import csv

    with open("Health-ClosedIssues0000.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append(row)

    best = remember(header, rows)
    print(f"Top {len(best)} trustworthy setups out of {len(rows)}:")
    for pos in best:
        print(f"  Row {pos}")
