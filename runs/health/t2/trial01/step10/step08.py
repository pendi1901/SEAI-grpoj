import csv


def fix(header, row, levers):
    """Fix a bad row by changing at least one lever within allowed values."""
    
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    input_cols = []
    for col in header:
        if col[0].isupper() and col not in goal_cols:
            input_cols.append(col)
    
    target_col = goal_cols[0]  # "MRE-"
    
    best_lever = None
    best_val = None
    
    # Try numeric levers first (especially N_estimators which is key)
    for col in ['N_estimators'] + [c for c in input_cols if c != 'N_estimators']:
        if col in levers and isinstance(levers[col], tuple):
            low, high = levers[col]
            mid = (low + high) / 2.0
            best_lever = col
            best_val = mid
    
    # Fallback to symbolic levers
    if best_lever is None:
        for col in header:
            if col[0].islower() and col not in goal_cols and col in levers:
                vals = levers[col]
                if isinstance(vals, list):
                    best_lever = col
                    best_val = vals[0]
    
    return {best_lever: best_val} if best_lever else {}


if __name__ == "__main__":
    with open("Health-ClosedIssues0000.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    # Find a bad row (worst by scoring like step01)
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    scored = []
    col_vals = {}
    for i, row in enumerate(rows):
        for col in goal_cols:
            val_str = row[header.index(col)]
            try:
                val = float(val_str)
            except ValueError:
                continue
            col_vals.setdefault(col, []).append((i, val))
    
    scored_rows = []
    for i in range(len(rows)):
        score = 0.0
        valid = True
        for col in goal_cols:
            vals = col_vals[col]
            mn = min(v[1] for v in vals)
            mx = max(v[1] for v in vals)
            val_str = rows[i][header.index(col)]
            try:
                val = float(val_str)
            except ValueError:
                valid = False
                break
            if col.endswith('-'):
                score += (mx - val) / (mx - mn + 1e-9)
            else:
                score += (val - mn) / (mx - mn + 1e-9)
        if not valid:
            continue
        scored_rows.append((i, score))
    
    scored_rows.sort(key=lambda x: x[1])
    worst_pos = scored_rows[-1][0]
    bad_row = rows[worst_pos]

    # Simulate what levers would be (since test harness provides them)
    # Just show the fix recommendation
    print(f"Current worst setup is row {worst_pos}")
    for col in header:
        print(f"  {col}: {bad_row[header.index(col)]}")

    # Demonstrate fix with hypothetical levers
    levers = {}
    for col in ['N_estimators', 'criterion', 'Min_sample_leaves', 'Max_depth']:
        idx = header.index(col)
        val_str = bad_row[idx]
        try:
            v = float(val_str)
        except ValueError:
            continue
        levers[col] = (v - 1, v + 1)

    fix_result = fix(header, bad_row, levers)
    print(f"\nRecommended fix:")
    for col, val in fix_result.items():
        print(f"  {col}: {val}")
