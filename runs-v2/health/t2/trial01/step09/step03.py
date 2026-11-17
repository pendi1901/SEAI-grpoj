from step01 import _to_float, remember


def certify(xs, ys):
    """Return True if xs and ys are the same apart from noise."""
    n_x = len(xs) or 1
    n_y = len(ys) or 1
    mean_x = sum(xs) / n_x
    mean_y = sum(ys) / n_y

    def std(vals):
        m = sum(vals) / len(vals)
        return (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5

    sx = std(xs) if xs else 1.0
    sy = std(ys) if ys else 1.0

    threshold = (sx + sy) * 2.0
    return abs(mean_x - mean_y) <= threshold


if __name__ == "__main__":
    import csv

    with open("Health-ClosedIssues0000.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            rows.append(row)

    minimise = [c for c in header if c.endswith('-')]
    maximise = [c for c in header if c.endswith('+')]
    goal_cols = minimise + maximise

    big_rows = []
    small_rows = []

    for row in rows:
        n_est = _to_float(row[header.index("N_estimators")])
        if n_est >= 50:
            big_rows.append(row)
        else:
            small_rows.append(row)

    def avg_goals(rows):
        if not rows:
            return [0.0] * len(goal_cols)
        n = len(rows)
        avg = []
        for col in goal_cols:
            vals = [_to_float(r[header.index(col)]) for r in rows]
            avg.append(sum(vals) / n)
        return avg

    big_avg = avg_goals(big_rows)
    small_avg = avg_goals(small_rows)

    result = certify(big_avg, small_avg)
    print(f"Big vs Small: {'Real difference' if not result else 'Noise'}")
