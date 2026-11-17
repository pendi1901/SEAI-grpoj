import csv


def fix(header, row, levers):
    """Recommend changes to keep an at-risk employee."""
    attrition_idx = header.index('attrition')
    goal_cols = [c for c in header if c.endswith('+')]
    years_col = 'YearsAtCompany+'

    # Current tenure values (use 0.0 when hidden)
    cur_goals = {}
    for col in goal_cols:
        cell = row[header.index(col)]
        try:
            cur_goals[col] = float(cell) if cell != '?' else 0.0
        except ValueError:
            cur_goals[col] = 0.0

    # Find the worst goal (smallest + value or largest - value).
    def score(v):
        return v if v is not None else 0.0

    best_col = max(goal_cols, key=lambda c: score(cur_goals.get(c)))

    # Decide which lever to use based on what's most impactful.
    chosen_lever = None
    new_val = None

    for col in goal_cols:
        cell = row[header.index(col)]
        if cell == '?':
            continue
        try:
            v = float(cell)
        except ValueError:
            continue

        # For '+' goals, higher is better; for '-' goals, lower is better.
        if col.endswith('+'):
            direction = 1.0
        else:
            direction = -1.0

        # Pick a lever that moves the goal in the right direction.
        if v < cur_goals.get(best_col, 0) * direction:
            chosen_lever = col
            new_val = v + direction * 5.0
            break

    # If no '+' goal was improved, try '-' goals (reduce attrition risk).
    if chosen_lever is None:
        for col in goal_cols:
            cell = row[header.index(col)]
            if cell == '?':
                continue
            try:
                v = float(cell)
            except ValueError:
                continue
            if col.endswith('-'):
                direction = -1.0
            else:
                direction = 1.0

            if v > cur_goals.get(best_col, 0) * direction:
                chosen_lever = col
                new_val = v + direction * 5.0
                break

    # If still nothing, default to increasing YearsAtCompany+ (the main goal).
    if chosen_lever is None:
        chosen_lever = 'YearsAtCompany+'
        cell = row[header.index(chosen_lever)]
        try:
            new_val = float(cell) + 5.0 if cell != '?' else 5.0
        except ValueError:
            new_val = 5.0

    # Ensure the value is within allowed range (levers dict).
    if chosen_lever in levers and isinstance(levers[chosen_lever], tuple):
        lo, hi = levers[chosen_lever]
        new_val = max(lo, min(hi, new_val))

    return {chosen_lever: str(new_val)}


if __name__ == '__main__':
    with open('WA_Fn-UseC_-HR-Employee-Attrition.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # Build allowed levers from the data.
    goal_cols = [c for c in header if c.endswith('+')]
    attrition_idx = header.index('attrition')

    levers = {}
    for col in goal_cols:
        vals = []
        for r in rows:
            cell = r[header.index(col)]
            try:
                vals.append(float(cell))
            except ValueError:
                pass
        if vals:
            lo, hi = min(vals), max(vals)
            levers[col] = (lo - 1.0, hi + 1.0)

    # Pick a bad row (attrition=Yes).
    bad_row = None
    for r in rows:
        if r[attrition_idx] == 'Yes':
            bad_row = r
            break

    result = fix(header, bad_row, levers)
    print(
        f"To retain an employee who left early, we should change "
        + f"{len(result)} lever(s): {', '.join(f'{k}={v}' for k, v in result.items())}"
    )
