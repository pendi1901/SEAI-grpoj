import sys
sys.path.insert(0, '.')
from step01 import remember


def fix(header, row, levers):
    goal_cols = [c for c in header if c.endswith('-')]

    # Load training data to find good configurations.
    df = __import__('pandas').read_csv('pom3a.train.csv')
    train_rows = [list(r) for _, r in df.iterrows()]

    best_positions = remember(header, train_rows)

    input_cols = [c for c in header if not c.endswith('-')]

    # For each lever, pick the value from top training setups that is closest to the current row.
    results = {}
    for col in levers:
        allowed = levers[col]

        candidates = []
        for i in best_positions[:20]:
            val = float(train_rows[i][header.index(col)])
            if isinstance(allowed, tuple):
                low, high = allowed
                if low <= val <= high:
                    candidates.append(val)

        if candidates:
            # Smallest change: pick the candidate closest to current value.
            results[col] = min(candidates, key=lambda v: abs(v - float(row[header.index(col)])))

    # Must have changed at least one lever; fallback to midpoint of allowed range.
    if not any(results.values()):
        for col in levers:
            allowed = levers[col]
            if isinstance(allowed, tuple):
                low, high = allowed
                results[col] = (low + high) / 2.0
                break

    return results


if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)

    rows = [list(r) for _, r in df.iterrows()]
    worst_idx = int(np.argmax([float(rows[i]['Cost-']) + float(rows[i]['Idle-']) for i in range(len(rows))]))

    test_row = list(rows[worst_idx])
    goal_cols = [c for c in header if c.endswith('-')]
    for col in goal_cols:
        test_row[header.index(col)] = '?'

    lever_map = {
        'Plan': (0.1, 0.9),
        'Team Size': (0.2, 0.8),
        'Culture': (0.01, 0.5),
        'Criticality Modifier': (0.3, 0.7),
        'Initial Known': (0.6, 0.95),
        'Inter-Dependency': (0.1, 0.4),
        'Dynamism': (0.0, 0.5),
        'Size': (0.2, 0.7),
    }

    result = fix(header, test_row, lever_map)
    print(f"Recommended changes: {result}")
