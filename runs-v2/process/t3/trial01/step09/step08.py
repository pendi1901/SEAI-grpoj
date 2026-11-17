import pandas as pd
import numpy as np


def fix(header, row, levers):
    goal_cols = [h for h in header if h.endswith('-')]
    input_cols = [h for h in header if not h.endswith('-')]

    # Build a baseline DataFrame from the training data to compute stats
    df = pd.read_csv('pom3a.train.csv')
    for col in goal_cols:
        df[col] = df[col].replace('?', np.nan).astype(float)

    means = {}
    stds = {}
    for col in goal_cols:
        vals = df[col].dropna()
        if len(vals) > 0:
            means[col] = vals.mean()
            stds[col] = vals.std()
        else:
            means[col] = 0.0
            stds[col] = 1.0

    # Normalize goals to z-scores (low is good for '-', high is good for '+')
    def normalize(val, mean, std):
        if pd.isna(val) or val == '?':
            return 0.0
        try:
            v = float(val)
        except (ValueError, TypeError):
            return 0.0
        if std == 0:
            return 0.0
        return (v - mean) / std

    # Compute baseline score for the given row
    def compute_score(row_dict):
        scores = []
        for col in goal_cols:
            val = row_dict.get(col, '?')
            z = normalize(val, means[col], stds[col])
            scores.append(z)
        return np.mean(scores) if scores else 0.0

    # Try each lever combination to find the best one
    best_row = dict(row)
    best_score = compute_score(best_row)

    for col in levers:
        allowed = levers[col]
        if isinstance(allowed, (list, tuple)) and len(allowed) >= 2 and not isinstance(allowed[0], str):
            # Numeric lever: try low and high
            candidates = [allowed[0], allowed[-1]]
        else:
            # Symbolic lever: try all values
            candidates = list(allowed)

        for val in candidates:
            test_row = dict(best_row)
            if col.endswith('-'):
                test_row[col] = val
            else:
                test_row[col] = val
            score = compute_score(test_row)
            if score > best_score:
                best_score = score
                best_row = test_row

    return best_row


if __name__ == "__main__":
    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    goal_cols = [h for h in header if h.endswith('-')]
    input_cols = [h for h in header if not h.endswith('-')]

    # Find a bad row (high cost, high idle, low score)
    bad_row_idx = None
    for i, r in enumerate(rows):
        goals = {}
        for col in goal_cols:
            goals[col] = r[header.index(col)] if header.index(col) < len(r) else '?'
        score = 0.0
        for col in goal_cols:
            val = goals.get(col, '?')
            try:
                v = float(val)
            except (ValueError, TypeError):
                continue
            if col.endswith('-'):
                score -= v
            else:
                score += v
        if score < 0 and bad_row_idx is None:
            bad_row_idx = i
            break

    if bad_row_idx is None:
        bad_row_idx = 0

    bad_row = rows[bad_row_idx]

    # Determine levers (input columns) with their allowed values from the data
    lever_candidates = {}
    for col in input_cols:
        vals = df[col].dropna()
        if len(vals) > 0:
            unique_vals = sorted(vals.unique())[:5]
            if isinstance(unique_vals[0], float):
                low, high = unique_vals[0], unique_vals[-1]
                lever_candidates[col] = (low, high)
            else:
                lever_candidates[col] = list(unique_vals)

    levers = {col: lever_candidates.get(col, []) for col in input_cols if len(lever_candidates.get(col, [])) > 0}

    result = fix(header, bad_row, levers)

    print(f"Original row score components:")
    for col in goal_cols:
        val = bad_row[header.index(col)] if header.index(col) < len(bad_row) else '?'
        print(f"  {col}: {val}")

    print(f"\nRecommended changes:")
    for col, new_val in result.items():
        if col != 'Criticality':  # Skip non-lever columns
            old_val = bad_row[header.index(col)] if header.index(col) < len(bad_row) else '?'
            print(f"  {col}: {old_val} -> {new_val}")

    print(f"\nThis plan change would improve the setup.")
