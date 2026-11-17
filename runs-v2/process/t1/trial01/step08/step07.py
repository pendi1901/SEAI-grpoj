import csv


def choose(header, rows, label):
    goal_cols = ['Cost-', 'Score-', 'Idle-']
    input_cols = [c for c in header if c not in goal_cols]

    def parse_row(row):
        result = {}
        ok = True
        for col in input_cols + goal_cols:
            idx = header.index(col)
            val = row[idx]
            if val == '?':
                return None
            try:
                result[col] = float(val)
            except ValueError:
                return None
        return result

    # Parse all rows (all have '?' goals, so we only get inputs)
    parsed = []
    for row in rows:
        p = parse_row(row)
        if p is not None:
            parsed.append(p)

    n = len(parsed)
    best_pos = 0
    best_score = float('inf')

    # Try all rows, but only evaluate up to 50 different label calls.
    # Since every row has '?' goals, we can't call label() meaningfully —
    # so we pick the row with the best input features (closest to ideal).
    # But wait: the problem says "Every goal cell in `rows` is '?'." So we have no info on goals.
    # We need to use label() to get true goals, but can call at most 50 times.
    # Strategy: try rows one by one, evaluate via label(), and pick best.

    for i in range(n):
        if len([i]) > 50:  # we've already used our budget? No — we need to track differently.
            break

    # Actually let me re-read: "you may label at most 50 different rows"
    # So I should try up to 50 rows, call label(i) for each, and pick best.
    # But which 50? Let's just try the first 50 (or all if fewer).

    candidates = []
    for i in range(min(n, 50)):
        goals = label(i)
        score = sum(goals[c] for c in goal_cols)  # lower is better since all end in -
        candidates.append((score, i))

    # Sort by score ascending (lower = better)
    candidates.sort(key=lambda x: x[0])

    return candidates[0][1]


if __name__ == "__main__":
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    best_pos = choose(header, rows, label)
    goals = label(best_pos)
    print(f"Best setup is at position {best_pos}: Cost-={goals['Cost-']:.4f}, Score-={goals['Score-']:.4f}, Idle-={goals['Idle-']:.4f}")
