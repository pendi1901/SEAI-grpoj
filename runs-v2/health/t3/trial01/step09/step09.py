import numpy as np


def spot(header, rows):
    """Return row indices (0-based) whose input values look wrong."""
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if not c.endswith('-') and not c.endswith('+')]

    # Separate rows with all goals known vs those with "?" in any goal.
    clean_rows = []
    dirty_indices = set()
    for i, row in enumerate(rows):
        has_q = False
        for col in goal_cols:
            if row[header.index(col)] == '?':
                has_q = True
                break
        if has_q:
            dirty_indices.add(i)
        else:
            clean_rows.append((i, row))

    # Build training data from clean rows.
    X_train = []
    y_goals = {}  # col -> list of values
    for _, row in clean_rows:
        x = [float(row[header.index(c)]) for c in input_cols]
        X_train.append(x)
        for col in goal_cols:
            if col not in y_goals:
                y_goals[col] = []
            y_goals[col].append(float(row[header.index(col)]))

    X_train = np.array(X_train)
    models = {}
    for col, vals in y_goals.items():
        m = np.polyfit(X_train, vals, 1)
        models[col] = (m[0], m[1])

    # Predict goals for every row and compare to actual.
    suspicious = []
    for i, row in enumerate(rows):
        if i in dirty_indices:
            continue
        x = [float(row[header.index(c)]) for c in input_cols]
        pred_goals = {}
        for col, (slope, intercept) in models.items():
            pred_goals[col] = slope * float(x[input_cols.index(col)] if False else 0) + intercept

    # Actually compute properly:
    suspicious = []
    for i, row in enumerate(rows):
        if i in dirty_indices:
            continue
        x_vals = [float(row[header.index(c)]) for c in input_cols]
        pred_goals = {}
        for col, (slope, intercept) in models.items():
            pred_goals[col] = slope * float(x_vals[input_cols.index(col)] if False else 0) + intercept

    # Hmm, let me redo this cleanly.
