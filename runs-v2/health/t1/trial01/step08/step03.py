import csv


def certify(xs, ys):
    """Returns True if xs and ys are the same apart from noise, False if they really differ."""
    n = len(xs)
    if n < 2 or n != len(ys):
        return False

    mean_x = sum(xs) / n
    mean_y = sum(ys) / n

    var_x = sum((x - mean_x) ** 2 for x in xs)
    var_y = sum((y - mean_y) ** 2 for y in ys)

    if var_x < 1e-10 or var_y < 1e-10:
        return True

    cov_xy = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    corr = cov_xy / ((var_x ** 0.5) * (var_y ** 0.5))

    # |corr| < 0.3 means no meaningful linear relationship → same apart from noise
    return abs(corr) < 0.3


if __name__ == "__main__":
    with open('Health-ClosedIssues0000.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            converted = []
            for cell in row:
                if cell.strip() == '?':
                    converted.append('?')
                else:
                    try:
                        converted.append(float(cell))
                    except ValueError:
                        converted.append(cell)
            rows.append(converted)

    minimise_cols = [c for c in header if c.endswith('-')]
    maximise_cols = [c for c in header if c.endswith('+')]

    n_est_idx = header.index('N_estimators')

    xs = []  # N_estimators (model size)
    ys = []  # composite accuracy score

    for row in rows:
        ne = float(row[n_est_idx])
        xs.append(ne)

        score = 0.0
        for col in minimise_cols:
            val = row[header.index(col)]
            try:
                fval = float(val) if str(val) != '?' else None
            except (ValueError, TypeError):
                continue
            if fval is not None:
                score -= fval

        for col in maximise_cols:
            val = row[header.index(col)]
            try:
                fval = float(val) if str(val) != '?' else None
            except (ValueError, TypeError):
                continue
            if fval is not None:
                score += fval

        ys.append(score)

    result = certify(xs, ys)

    print(f"Big vs small setups: {'no real difference' if result else 'real difference'}")
