import csv


def remember(header, rows):
    # Identify goal columns: '-' → minimise, '+' → maximise
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]

    # Pass 1 – collect numeric values per goal column; mark rows with any '?' as invalid
    col_vals = {}
    row_valid = [True] * len(rows)
    for i, row in enumerate(rows):
        for col in goal_cols:
            val_str = row[header.index(col)]
            if val_str == '?' or val_str is None:
                row_valid[i] = False
            else:
                try:
                    val = float(val_str)
                except ValueError:
                    row_valid[i] = False
                    break
                col_vals.setdefault(col, []).append((i, val))

    # Pass 2 – normalise each goal to [0,1] and sum; higher is better
    scored = []
    for i in range(len(rows)):
        if not row_valid[i]:
            continue
        score = 0.0
        for col in goal_cols:
            vals = col_vals[col]
            mn = min(v[1] for v in vals)
            mx = max(v[1] for v in vals)
            val_str = row[header.index(col)]
            val = float(val_str)
            if col.endswith('-'):          # minimise → low is best
                score += (mx - val) / (mx - mn + 1e-9)
            else:                          # maximise → high is best
                score += (val - mn) / (mx - mn + 1e-9)
        scored.append((i, score))

    scored.sort(key=lambda x: -x[1])
    n = len(scored)
    k = max(1, int(n * 0.05))           # at most 5% of rows
    return [pos for pos, _ in scored[:k]]


if __name__ == "__main__":
    with open("Health-ClosedIssues0000.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    result = remember(header, rows)
    print(f"Best {len(result)} of {len(rows)} setups:")
    for pos in result:
        print(f"  Row {pos}")
