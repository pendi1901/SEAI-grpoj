def justify(header, rows, row):
    """Return (p, reason) where p is the fraction of `rows` that this setup beats."""
    goals = [c for c in header if c.endswith('-')]

    # Compute min/max per goal across all existing rows
    goal_mins = {}
    goal_maxs = {}
    n_rows = len(rows)
    for g in goals:
        vals = []
        for r in rows:
            v = float(r[header.index(g)])
            vals.append(v)
        goal_mins[g] = min(vals)
        goal_maxs[g] = max(vals)

    # Count how many existing rows are worse than an ideal hypothetical row (score=0)
    better_count = 0
    for r in rows:
        total_score = 0.0
        for g in goals:
            v = float(r[header.index(g)])
            if goal_maxs[g] == goal_mins[g]:
                norm = 0.0
            else:
                norm = (v - goal_mins[g]) / (goal_maxs[g] - goal_mins[g])
            total_score += norm
        if total_score > 0:
            better_count += 1

    p = better_count / n_rows

    if p >= 0.95:
        reason = "This setup would be in the top tier, beating most others."
    elif p >= 0.8:
        reason = "This setup is strong, outperforming a large majority of alternatives."
    elif p >= 0.6:
        reason = "This setup performs well above average compared to existing setups."
    else:
        reason = "This setup would rank below most existing configurations."

    return (p, reason)


if __name__ == "__main__":
    import csv

    with open('pom3a.train.csv', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            if len(row) == len(header):
                rows.append(row)

    # Build a hypothetical row by replacing goal cells of the first data row with "?"
    goals = [c for c in header if c.endswith('-')]
    sample_row = list(rows[0])
    for g in goals:
        idx = header.index(g)
        sample_row[idx] = '?'

    p, reason = justify(header, rows, sample_row)
    print(f"Rank: {p:.1%} of existing setups are worse than this ideal configuration.")
    print(reason)
