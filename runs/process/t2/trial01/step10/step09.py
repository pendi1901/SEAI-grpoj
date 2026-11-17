def spot(header, rows):
    goal_cols = ['Cost-', 'Score-', 'Idle-']

    def is_goal(col):
        return col.endswith('-') and col != '-'

    n = len(rows)
    if n == 0:
        return []

    # Determine column type (numeric vs symbolic) from non-goal columns.
    col_types = {}
    for col in header:
        if is_goal(col):
            continue
        vals = [row[header.index(col)] for row in rows]
        numeric_count = sum(1 for v in vals if isinstance(v, (int, float)) and v != '?')
        col_types[col] = 'numeric' if numeric_count == len(vals) else 'symbolic'

    suspicious_rows = []

    for i, row in enumerate(rows):
        reasons = []
        for col in header:
            if is_goal(col) or col == '-':
                continue
            val = row[header.index(col)]
            if val == '?':
                continue

            ctype = col_types[col]

            if ctype == 'numeric':
                # Collect numeric values from all rows for this column.
                num_vals = []
                for r in rows:
                    v = r[header.index(col)]
                    if isinstance(v, (int, float)) and v != '?':
                        num_vals.append(float(v))

                if not num_vals:
                    continue

                mean_val = sum(num_vals) / len(num_vals)
                var_val = sum((v - mean_val) ** 2 for v in num_vals) / max(len(num_vals) - 1, 1)
                std_val = var_val ** 0.5

                if std_val > 0:
                    z = abs(float(val) - mean_val) / std_val
                    if z > 3.0:
                        reasons.append(col)

            elif ctype == 'symbolic':
                # Check if this value appears in any other row for this column.
                seen_values = set()
                for r in rows:
                    v = r[header.index(col)]
                    if isinstance(v, str) and v != '?':
                        seen_values.add(v)

                if val not in seen_values:
                    reasons.append(col)

        if reasons:
            suspicious_rows.append(i)

    return suspicious_rows


if __name__ == "__main__":
    import csv

    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [list(map(float, row)) for row in reader]

    suspicious = spot(header, rows)
    print(f"Suspicious rows (most likely mistyped/made up): {suspicious}")
