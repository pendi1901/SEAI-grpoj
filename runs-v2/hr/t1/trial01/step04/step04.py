def flow(header, row, seen):
    """Return True if this employee needs a retention conversation."""
    attrition_idx = header.index('attrition')
    years_col = 'YearsAtCompany+'
    years_idx = header.index(years_col)

    n_seen = len(seen)
    if n_seen == 0:
        return False

    # Compute tenure stats from seen rows
    year_vals = []
    for r in seen:
        try:
            year_vals.append(float(r[years_idx]))
        except (ValueError, TypeError):
            pass

    mean_y = sum(year_vals) / len(year_vals) if year_vals else 0.0
    var_y = sum((v - mean_y) ** 2 for v in year_vals) / len(year_vals) if year_vals else 1.0
    std_y = var_y ** 0.5

    # Current row's tenure
    try:
        cur_y = float(row[years_idx])
    except (ValueError, TypeError):
        return False

    # Flag attrition cases and low-tenure at-risk cases
    if row[attrition_idx] == 'Yes':
        return True

    if std_y > 0 and mean_y - 2 * std_y < cur_y < mean_y + 1.5 * std_y:
        return True

    return False


if __name__ == '__main__':
    with open('WA_Fn-UseC_-HR-Employee-Attrition.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    flagged = []
    for row in rows:
        if flow(header, row, flagged):
            flagged.append(row)

    print(
        f"Out of {len(rows)} staff records, "
        f"{len(flagged)} need a retention conversation."
    )
