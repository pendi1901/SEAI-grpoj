def justify(header, rows, row):
    """Compare a test setup (with ? goals) against all training setups."""

    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    is_numeric = [c[0].isupper() for c in header]

    def to_float(cell):
        try:
            return float(cell)
        except (ValueError, TypeError):
            return 0.0

    n = len(rows)

    # Compute best/worst per goal column from training data
    best_vals = []
    worst_vals = []
    for gcol in goal_cols:
        vals = [to_float(r[header.index(gcol)]) for r in rows]
        best_vals.append(min(vals))
        worst_vals.append(max(vals))

    # Estimate goals for test row using nearest-neighbour on non-goal numeric columns
    goal_estimates = []
    for gcol in goal_cols:
        best_dist = float('inf')
        best_val = None
        for i, train_row in enumerate(rows):
            dist = 0.0
            for j in range(len(header)):
                if not is_numeric[j]:
                    continue
                if j == header.index(gcol):
                    continue
                tv = to_float(train_row[j])
                rv = to_float(row[j])
                diff = tv - rv
                dist += diff * diff
            if dist < best_dist:
                best_dist = dist
                best_val = to_float(train_row[header.index(gcol)])
        goal_estimates.append(best_val)

    # Score a row on its goals using normalized scoring (best=1, worst=0)
    def score_row(vals):
        s = 0.0
        for j, gcol in enumerate(goal_cols):
            v = vals[j]
            if gcol.endswith('-'):
                denom = best_vals[j] - worst_vals[j]
                if denom <= 0:
                    return 1.0
                else:
                    s += (v - worst_vals[j]) / denom
            else:
                denom = best_vals[j] - worst_vals[j]
                if denom <= 0:
                    return 1.0
                else:
                    s += (best_vals[j] - v) / denom
        return s / len(goal_cols)

    test_score = score_row(goal_estimates)

    # Count how many training rows have lower scores (i.e., are worse)
    beaten_count = 0
    for i, train_row in enumerate(rows):
        vals = [to_float(train_row[header.index(gcol)]) for gcol in goal_cols]
        train_score = score_row(vals)
        if test_score > train_score:
            beaten_count += 1

    p = beaten_count / n

    reason = f"This setup is better than {p:.0%} of all training setups."
    return (p, reason)


if __name__ == "__main__":
    import csv

    with open("Health-ClosedIssues0000.train.csv") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(10000)]

    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    goal_indices = [header.index(c) for c in goal_cols]

    # Create a test row by taking the first training row and replacing goals with "?"
    test_row = list(rows[0])
    for idx in goal_indices:
        test_row[idx] = "?"

    p, reason = justify(header, rows, test_row)
    print(f"{reason} ({p:.1%})")
