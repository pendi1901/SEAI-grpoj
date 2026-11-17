import csv


def certify(xs, ys):
    """Return True if xs and ys are essentially the same apart from noise."""
    n = len(xs) + len(ys)
    if n == 0:
        return False
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    all_vals = xs + ys
    overall_mean = sum(all_vals) / n
    var = sum((v - overall_mean) ** 2 for v in all_vals) / n
    std = var ** 0.5
    diff = abs(mean_x - mean_y)
    if std > 0:
        return diff < 1.5 * std
    return False


def main():
    with open('WA_Fn-UseC_-HR-Employee-Attrition.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    over_idx = header.index('overTime')
    years_col = 'YearsAtCompany+'
    years_idx = header.index(years_col)

    group_x = []  # overtime workers
    group_y = []  # non-overtime workers

    for row in rows:
        ot = row[over_idx]
        if ot not in ('Y', 'N'):
            continue
        v = float(row[years_idx])
        if ot == 'Y':
            group_x.append(v)
        else:
            group_y.append(v)

    avg_x = sum(group_x) / len(group_x) if group_x else 0.0
    avg_y = sum(group_y) / len(group_y) if group_y else 0.0

    print(
        f"Overtime workers ({len(group_x)}): avg {avg_x:.1f} years at company\n"
        f"No overtime workers ({len(group_y)}): avg {avg_y:.1f} years at company\n"
        f"Their tenure is {'similar' if certify([avg_x], [avg_y]) else 'different'} apart from noise."
    )


if __name__ == '__main__':
    main()
