import csv


def fix(header, row, levers):
    """Return {column: new_value} for the smallest change that rescues a bad setup."""
    goal_cols = ['Cost-', 'Score-', 'Idle-']
    input_cols = [c for c in header if c not in goal_cols]

    # Identify which columns are numeric (uppercase start) vs symbolic (lowercase).
    # Per spec: upper-case-start => numeric, lower-case-start => symbolic.
    is_numeric = {}
    for col in header:
        try:
            float(col[0])  # dummy check — actually we just look at first char
        except Exception:
            pass

    def is_upper_start(name):
        return name and name[0].isupper()

    numeric_cols = [c for c in header if is_upper_start(c)]
    symbolic_cols = [c for c in header if not is_upper_start(c)]

    # Determine goal direction: ends with '-' => minimise; '+' => maximise.
    def goal_direction(col):
        return 'min' if col.endswith('-') else 'max'

    # Parse the current row's goals (they may be '?' — but in this scenario we know it's bad).
    cur_goals = {}
    for col in goal_cols:
        idx = header.index(col)
        val = row[idx]
        try:
            cur_goals[col] = float(val)
        except ValueError:
            cur_goals[col] = None

    # Parse all training rows' goals to find the best achievable values.
    train_rows = []
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header_line = next(reader)  # skip — we already have header from caller? No, caller gives header.
        # Actually the function receives `header` directly. We need to read the file for training data.
        pass

    # Re-read the CSV to get all training rows (excluding current row).
    train_data = []
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header — but wait, we already have `header` from caller. The CSV has its own header.
        for r in reader:
            train_data.append(r)

    # Parse training goals to find best achievable values per goal column.
    best_goals = {}
    for col in goal_cols:
        vals = []
        for tr in train_data:
            idx = header.index(col)
            val = tr[idx]
            if val == '?':
                continue
            try:
                vals.append(float(val))
            except ValueError:
                continue
        if vals:
            best_goals[col] = min(vals) if goal_direction(col) == 'min' else max(vals)
        else:
            # Fallback to current value or 0.
            best_goals[col] = cur_goals.get(col, 0.0)

    # Now determine which levers we can change and pick the smallest set that improves goals.
    changes = {}
    for col in goal_cols:
        if col in levers:
            low, high = levers[col]
            target = best_goals.get(col, cur_goals.get(col))
            # Choose value closest to target within allowed range.
            if isinstance(low, (int, float)) and isinstance(high, (int, float)):
                new_val = max(low, min(high, target))
                changes[col] = new_val

    # If no goal columns are in levers, try input columns that can be changed to improve goals.
    if not changes:
        for col in header:
            if col in levers and col not in goal_cols:
                low, high = levers[col]
                cur_val = row[header.index(col)]
                try:
                    fcur = float(cur_val)
                except ValueError:
                    continue
                # Pick value that minimises distance to target (which we don't know exactly).
                # Heuristic: pick midpoint if no goal info, or best available.
                mid = (low + high) / 2.0
                changes[col] = mid

    return changes


if __name__ == "__main__":
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    # Pick a bad row (high Cost-, low Score-, high Idle-).
    worst_idx = 0
    worst_score = float('inf')
    for i, r in enumerate(rows):
        goals = {}
        ok = True
        for col in ['Cost-', 'Score-', 'Idle-']:
            idx = header.index(col)
            val = r[idx]
            try:
                goals[col] = float(val)
            except ValueError:
                ok = False
                break
        if not ok:
            continue
        s = goals['Cost-'] + goals['Score-'] + goals['Idle-']
        if s < worst_score:
            worst_score = s
            worst_idx = i

    bad_row = rows[worst_idx]
    print(f"Bad row {worst_idx}: Cost-={bad_row[header.index('Cost-')]:.4f}, "
          f"Score-={bad_row[header.index('Score-')]:.4f}, Idle-={bad_row[header.index('Idle-')]:.4f}")

    # Determine levers from the row's current values — allow changing any numeric column.
    levers = {}
    for col in header:
        idx = header.index(col)
        val = bad_row[idx]
        try:
            fval = float(val)
            if col.endswith('-'):
                # Goals: allow a range around current value.
                lo = max(0.0, fval * 0.8)
                hi = min(fval * 1.2, 1.0)
                levers[col] = (lo, hi)
            else:
                # Numeric input columns: allow ±20% or full range if near boundaries.
                lo = max(0.0, fval * 0.8)
                hi = min(fval * 1.2, 1.0)
                levers[col] = (lo, hi)
        except ValueError:
            # Symbolic column — allow current value as only option? But spec says list of strings.
            pass

    result = fix(header, bad_row, levers)
    print("Recommended changes:", result)
