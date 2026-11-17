import csv


def spot(header, rows):
    """Return row indices whose input values look wrong (entered wrongly)."""

    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]

    # Numeric input columns: uppercase, not a goal column
    input_cols = []
    for col in header:
        if col[0].isupper() and col not in goal_cols:
            input_cols.append(col)

    target_col = goal_cols[0]  # "MRE-"

    # Collect all known MRE- values to find the global range (excluding '?')
    mre_vals = []
    for row in rows:
        mre_str = row[header.index(target_col)]
        try:
            v = float(mre_str)
            mre_vals.append(v)
        except ValueError:
            pass

    if not mre_vals:
        return []

    mre_min = min(mre_vals)
    mre_max = max(mre_vals)
    mre_range = mre_max - mre_min + 1e-9

    # For each row, check whether its numeric inputs are plausible.
    # A "wrong entry" is a numeric input that lies far outside the range
    # of other rows' values for that column — i.e., an outlier in the
    # feature space. We flag such rows as suspicious.
    suspicious = []

    col_ranges = {}  # col -> (min, max) over all valid rows
    for row in rows:
        for col in input_cols:
            try:
                v = float(row[header.index(col)])
            except ValueError:
                continue
            col_ranges.setdefault(col, []).append(v)

    col_mins = {col: min(vals) for col, vals in col_ranges.items()}
    col_maxs = {col: max(vals) for col, vals in col_ranges.items()}

    # A row is suspicious if any of its numeric inputs falls outside the
    # typical range (more than 3 standard deviations from the column mean).
    import math

    col_means = {col: sum(vals) / len(vals) for col, vals in col_ranges.items()}
    col_stds = {}
    for col, vals in col_ranges.items():
        m = col_means[col]
        variance = sum((v - m) ** 2 for v in vals) / len(vals)
        col_stds[col] = math.sqrt(variance + 1e-9)

    for i, row in enumerate(rows):
        for col in input_cols:
            try:
                v = float(row[header.index(col)])
            except ValueError:
                continue
            mean = col_means[col]
            std = col_stds[col]
            if std > 0 and abs(v - mean) > 3 * std:
                suspicious.append(i)
                break

    # Also flag rows where MRE- is '?' — those are clearly incomplete/failed.
    for i, row in enumerate(rows):
        mre_str = row[header.index(target_col)]
        if mre_str == '?':
            suspicious.append(i)

    suspicious.sort()
    return suspicious


if __name__ == "__main__":
    with open("Health-ClosedIssues0000.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    bad = spot(header, rows)
    print(f"Rows that look like failed runs ({len(bad)} found):")
    for pos in bad:
        print(f"  Row {pos}")
