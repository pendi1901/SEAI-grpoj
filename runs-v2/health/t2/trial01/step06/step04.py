from step01 import _to_float, remember


def flow(header, row, seen):
    """Return True when the current row is good enough to ship."""
    minimise = [c for c in header if c.endswith('-')]
    maximise = [c for c in header if c.endswith('+')]

    # First row: nothing to compare against yet.
    if not seen:
        return False

    # Best goals so far (minimise → low, maximise → high).
    best = {}
    for col in minimise + maximise:
        vals = [_to_float(r[header.index(col)]) for r in seen]
        best[col] = min(vals) if col in minimise else max(vals)

    cur = {col: _to_float(row[header.index(col)]) for col in minimise + maximise}

    # Within tolerance of the best seen so far.
    tol = 0.15
    return all(
        (cur[col] - best[col]) <= tol if col in minimise else (best[col] - cur[col]) <= tol
        for col in minimise + maximise
    )


if __name__ == "__main__":
    import csv

    with open("Health-ClosedIssues0000.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append(row)

    # Use the top trustworthy setups from step01 to set expectations.
    best_rows = remember(header, rows)
    print(f"Top {len(best_rows)} reference setups identified.")

    for i, row in enumerate(rows):
        if flow(header, row, rows[:i]):
            print(f"Row {i} is good enough to ship!")
            break
    else:
        print("No suitable row found among the data.")
