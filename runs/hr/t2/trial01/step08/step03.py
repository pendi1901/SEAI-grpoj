import csv


def remember(header, rows):
    """From step01.py - kept as-is."""
    goal_cols = [c for c in header if c.endswith('+')]

    best_positions = []
    for i, row in enumerate(rows):
        score = 0
        valid = True
        for col in goal_cols:
            val = row[header.index(col)]
            if val == '?':
                valid = False
                break
            try:
                score += float(val)
            except ValueError:
                valid = False
                break
        if not valid:
            continue
        best_positions.append((score, i))

    best_positions.sort(reverse=True)

    max_count = max(1, int(len(rows) * 0.05))
    return [int(pos) for _, pos in best_positions[:max_count]]


def certify(xs, ys):
    """Returns True if xs and ys are the same apart from noise."""
    n_x, n_y = len(xs), len(ys)
    if n_x < 2 or n_y < 2:
        return False

    mean_x = sum(xs) / n_x
    mean_y = sum(ys) / n_y
    var_x = sum((v - mean_x) ** 2 for v in xs) / (n_x - 1) if n_x > 1 else 0.0
    var_y = sum((v - mean_y) ** 2 for v in ys) / (n_y - 1) if n_y > 1 else 0.0

    se = ((var_x / n_x) + (var_y / n_y)) ** 0.5
    t_stat = abs(mean_x - mean_y) / se if se > 0 else 0.0

    return t_stat < 2.0


if __name__ == "__main__":
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    goal_cols = [c for c in header if c.endswith('+')]
    feature_cols = [c for c in header if not c.endswith('+') and c != 'overTime']

    overtime_rows = []
    non_overtime_rows = []
    for row in rows:
        ot = row[header.index('overTime')]
        goal_vals = [float(row[header.index(c)]) for c in goal_cols]
        if ot == 'Y':
            overtime_rows.append(goal_vals)
        else:
            non_overtime_rows.append(goal_vals)

    xs = []
    ys = []
    for vals in overtime_rows:
        xs.extend(vals)
    for vals in non_overtime_rows:
        ys.extend(vals)

    result = certify(xs, ys)
    print(f"Overtime vs no-overtime tenure difference is {'real' if not result else 'noise'}." )
