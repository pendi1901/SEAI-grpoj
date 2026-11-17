import csv


def fix(header, row, levers):
    """Return {column: new_value} for the smallest change that makes `row` acceptable."""

    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    is_numeric = [c[0].isupper() for c in header]

    def to_float(cell):
        try:
            return float(cell)
        except (ValueError, TypeError):
            return 0.0

    # Identify which goal columns are hidden ("?") and which we can change
    hidden_goals = []
    changeable = {}  # col -> list of allowed values
    for c in header:
        if c.endswith('-') or c.endswith('+'):
            idx = header.index(c)
            val = row[idx]
            if val == "?":
                hidden_goals.append((c, idx))
        else:
            if c in levers:
                changeable[c] = levers[c]

    # If no goals are hidden and nothing is changeable, we can't fix it
    if not hidden_goals and not changeable:
        return {}

    # Load training data for reference best/worst per goal column
    with open("Health-ClosedIssues0000.train.csv") as f:
        reader = csv.reader(f)
        header_read = next(reader)
        train_rows = [next(reader) for _ in range(1000)]

    # Compute best and worst values per goal column from training data
    best_vals = []
    worst_vals = []
    for c in goal_cols:
        vals = [to_float(r[header_read.index(c)]) for r in train_rows]
        best_vals.append(min(vals))
        worst_vals.append(max(vals))

    # Score the current row on its goals (using "?" -> 0.0 as placeholder)
    def score_row(row):
        s = 0.0
        n_goals = len(goal_cols)
        for j, c in enumerate(goal_cols):
            v = to_float(row[header.index(c)]) if not any(
                row[header.index(gc)] == "?" for gc in goal_cols
            ) else 0.0
            if c.endswith('-'):
                denom = best_vals[j] - worst_vals[j]
                if denom <= 0:
                    s += 1.0
                else:
                    s += (v - worst_vals[j]) / denom
            else:
                denom = best_vals[j] - worst_vals[j]
                if denom <= 0:
                    s += 1.0
                else:
                    s += (best_vals[j] - v) / denom
        return s / n_goals

    # Try changing one lever at a time, picking the smallest change that improves score enough
    current_score = score_row(row)
    target = max(current_score + 0.1, 0.5)  # aim for at least modest improvement

    best_change = None
    best_new_score = current_score

    # Try each lever with its allowed values
    for col in header:
        if col not in levers:
            continue
        allowed = levers[col]
        idx = header.index(col)
        is_num = is_numeric[idx]

        for new_val in allowed:
            test_row = list(row)
            test_row[idx] = str(new_val)

            # Re-score with "?" goals replaced by 0.0 (same as before)
            s = score_row(test_row)
            if s > best_new_score and s >= target:
                change_size = abs(to_float(col) - to_float(new_val)) if is_num else len(str(new_val))
                # Prefer smallest absolute change
                if best_change is None or (change_size < 1e9):
                    best_change = {col: new_val}
                    best_new_score = s

    # If no single lever change reaches target, try combinations of two levers
    if best_change is None and len(changeable) >= 2:
        cols_to_try = list(changeable.keys())
        for i in range(len(cols_to_try)):
            for j in range(i + 1, len(cols_to_try)):
                c1, c2 = cols_to_try[i], cols_to_try[j]
                idx1 = header.index(c1)
                idx2 = header.index(c2)

                best_s = current_score
                best_combo = None
                for v1 in changeable[c1]:
                    for v2 in changeable[c2]:
                        test_row = list(row)
                        test_row[idx1] = str(v1)
                        test_row[idx2] = str(v2)
                        s = score_row(test_row)
                        if s > best_s:
                            best_s = s
                            best_combo = {c1: v1, c2: v2}

                if best_combo and best_s >= target:
                    best_change = best_combo
                    best_new_score = best_s

    # If still nothing, try all single-lever changes regardless of score (pick any improvement)
    if best_change is None:
        for col in header:
            if col not in levers:
                continue
            allowed = levers[col]
            idx = header.index(col)
            is_num = is_numeric[idx]

            for new_val in allowed:
                test_row = list(row)
                test_row[idx] = str(new_val)
                s = score_row(test_row)
                if s > best_new_score:
                    change_size = abs(to_float(col) - to_float(new_val)) if is_num else len(str(new_val))
                    if best_change is None or (change_size < 1e9):
                        best_change = {col: new_val}
                        best_new_score = s

    return best_change


if __name__ == "__main__":
    import csv

    with open("Health-ClosedIssues0000.train.csv") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(100)]

    # Pick the worst row (highest MRE-)
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    mre_idx = header.index("MRE-")

    worst_row = None
    worst_val = -1e9
    for row in rows:
        v = float(row[mre_idx])
        if v > worst_val:
            worst_val = v
            worst_row = row

    # Define levers (numeric columns with reasonable ranges, symbolic with common values)
    numeric_cols = [c for c in header if c[0].isupper() and not any(c.endswith(x) for x in ['-', '+'])]
    lever_ranges = {}
    for col in numeric_cols:
        idx = header.index(col)
        vals = []
        for row in rows:
            try:
                vals.append(float(row[idx]))
            except ValueError:
                pass
        if vals:
            lo, hi = min(vals), max(vals)
            lever_ranges[col] = (lo - 10, hi + 10)

    symbolic_cols = [c for c in header if not c[0].isupper() and not any(c.endswith(x) for x in ['-', '+'])]
    lever_symbols = {}
    for col in symbolic_cols:
        vals = set()
        for row in rows:
            vals.add(row[header.index(col)])
        lever_symbols[col] = sorted(vals, key=lambda x: (x == '?', x))

    levers = {col: range_val for col, range_val in lever_ranges.items()}
    levers.update(lever_symbols)

    fix_result = fix(header, worst_row, levers)

    if fix_result:
        print(f"Fix: change {len(fix_result)} setting(s):")
        for col, val in fix_result.items():
            print(f"  {col} -> {val}")
    else:
        print("No acceptable fix found.")
