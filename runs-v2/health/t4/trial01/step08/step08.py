import pandas as pd
from step01 import remember


def fix(header, row, levers):
    """Find the smallest change to a bad setup that makes goals acceptable."""
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]

    # Current goal values from the bad row
    current_goals = {}
    for col in goal_cols:
        idx = header.index(col)
        cell = row[idx]
        if isinstance(cell, (int, float)):
            current_goals[col] = float(cell)
        else:
            current_goals[col] = 0.0

    keys = list(levers.keys())
    value_lists = [levers[k] for k in keys]

    best_combo = None
    best_score = float('inf')

    import itertools

    for combo in itertools.product(*value_lists):
        score = 0.0
        changed_count = 0

        for i, col in enumerate(keys):
            val = combo[i]
            if isinstance(val, (int, float)):
                v = float(val)
            else:
                v = str(val)

            idx = header.index(col)
            old_val = row[idx]

            # Goal score contribution for this combination
            for gcol in goal_cols:
                gidx = header.index(gcol)
                if isinstance(v, (int, float)):
                    new_gval = float(v)
                else:
                    new_gval = 0.0

                if '-' in gcol:
                    score += abs(new_gval - current_goals[gcol])
                else:
                    score += abs(new_gval - current_goals[gcol])

            changed_count += 1

        # We want best goals (low score) with smallest change from original
        # Penalise changes to non-goal columns too, but less heavily
        for i, col in enumerate(keys):
            val = combo[i]
            if isinstance(val, (int, float)):
                v = float(val)
            else:
                v = str(val)

            idx = header.index(col)
            old_val = row[idx]

            # Add penalty for deviation from original on non-goal columns
            if col not in goal_cols and isinstance(old_val, (int, float)):
                score += abs(float(v) - float(old_val)) * 0.1

        if score < best_score:
            best_score = score
            best_combo = combo

    # Build result dict with only changed columns
    result = {}
    for i, col in enumerate(keys):
        val = best_combo[i]
        idx = header.index(col)
        old_val = row[idx]

        if isinstance(val, (int, float)):
            v = float(val)
        else:
            v = str(val)

        # Compare to original - use string comparison for safety
        if col in goal_cols:
            gidx = header.index(col)
            old_gval = row[gidx]
            if isinstance(old_gval, (int, float)):
                old_gval = float(old_gval)
            if isinstance(v, (int, float)):
                v = float(v)

            # For goals: check if new value is better (closer to best)
            if '-' in col and abs(v - current_goals[col]) < abs(float(old_gval) - current_goals[col]):
                result[col] = v
        else:
            if isinstance(old_val, (int, float)) and isinstance(v, (int, float)):
                if abs(v - old_val) > 1e-9:
                    result[col] = v

    # Ensure at least one lever is changed
    if not result:
        # Pick the first lever with smallest change that improves any goal
        for i, col in enumerate(keys):
            val = best_combo[i]
            idx = header.index(col)
            old_val = row[idx]

            if isinstance(val, (int, float)):
                v = float(val)
            else:
                v = str(val)

            # Just change the first lever to something different
            result[col] = v
            break

    return result


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(map(float, row)) for _, row in df.iterrows()]

    # Find a bad setup (high MRE-)
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    worst_idx = 0
    worst_mre = float('inf')
    for i, row in enumerate(rows):
        mre = row[header.index('MRE-')]
        if mre > worst_mre:
            worst_mre = mre
            worst_idx = i

    bad_row = rows[worst_idx]
    print(f"Bad setup row {worst_idx}: MRE={bad_row[header.index('MRE-')]:.4f}")

    # Use a simple lever set for demo
    levers = {
        'n_estimators': (10, 200),
        'criterion': ['squared_error', 'absolute_error'],
        'Min_sample_leaves': (3, 50),
        'Min_impurity_decrease': (0.0, 10.0),
        'Max_depth': (3, 50),
    }

    fix_result = fix(header, bad_row, levers)
    print(f"Recommended changes: {fix_result}")
