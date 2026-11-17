import csv


def spot(header, rows):
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

    parsed = []
    for i, row in enumerate(rows):
        p = parse_row(row)
        if p is not None:
            parsed.append((i, p))

    n = len(parsed)
    if n == 0:
        return []

    # For each goal column, find the best value seen (min since all end in -).
    best_goals = {}
    for col in goal_cols:
        vals = [p[col] for _, p in parsed]
        best_goals[col] = min(vals)

    # Score each row: how far its goals are from the best achievable.
    def goal_distance(p):
        return sum((best_goals[c] - p[c]) ** 2 for c in goal_cols)

    distances = [(goal_distance(p), i, p) for i, p in parsed]
    distances.sort(key=lambda x: x[0], reverse=True)

    # The top rows are the best. Now look at input columns and find outliers.
    # For each input column, compute median and MAD; flag rows far from typical.
    col_stats = {}
    for col in input_cols:
        vals = [p[col] for _, p in parsed if isinstance(p[col], (int, float))]
        if not vals:
            continue
        sorted_vals = sorted(vals)
        med = sorted_vals[len(sorted_vals) // 2]
        mad = sum(abs(v - med) for v in sorted_vals) / len(sorted_vals)
        col_stats[col] = (med, mad)

    suspicious = []
    for i, p in parsed:
        score = goal_distance(p)
        # Also check how far its inputs are from typical values.
        input_deviation = 0.0
        count = 0
        for col in input_cols:
            if isinstance(p[col], (int, float)):
                med, mad = col_stats[col]
                dev = abs(p[col] - med) / (mad + 1e-9)
                input_deviation += dev
                count += 1
        avg_dev = input_deviation / count if count > 0 else 0.0

        # Combine: rows that are both goal-outliers and input-outliers are most suspicious.
        # But actually, the customer says "input value that was entered wrongly" — so we want rows where inputs don't match typical patterns.
        # Let's flag rows with high average deviation on inputs.
        if avg_dev > 2.0:
            suspicious.append((avg_dev, i))

    # Sort by suspicion descending; return row indices most suspicious first.
    suspicious.sort(key=lambda x: -x[0])
    return [i for _, i in suspicious[:10]]


if __name__ == "__main__":
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    flagged = spot(header, rows)
    print(f"Found {len(flagged)} suspicious rows out of {len(rows)}:")
    for pos in flagged[:10]:
        c = float(rows[pos][header.index('Cost-')])
        s = float(rows[pos][header.index('Score-')])
        i = float(rows[pos][header.index('Idle-')])
        print(f"  Row {pos}: Cost-={c:.4f}, Score-={s:.4f}, Idle-={i:.4f}")
