import sys
sys.path.insert(0, '.')
from step01 import remember


def justify(header, rows, row):
    """Returns (p, reason) where p is fraction of rows that row beats."""
    
    goals = [h for h in header if h.endswith('-') or h.endswith('+')]
    numeric_cols = [c for c in header if c.isupper()]
    symbolic_cols = [c for c in header if not c.isupper() and not c.endswith('-') and not c.endswith('+')]

    def encode_row(row):
        return (tuple(float(row[header.index(c)]) for c in numeric_cols),
                tuple(row[header.index(c)] for c in symbolic_cols))

    # Predict goals for the test row using nearest neighbor on non-goal features.
    train_enc = [encode_row(r) for r in rows if not any(v == '?' for v in r)]
    test_enc = encode_row(row)

    best_match_idx = None
    best_dist = float('inf')

    for i, enc in enumerate(train_enc):
        dist = 0.0
        for c in header:
            if c.endswith('-') or c.endswith('+'):
                continue
            tv = test_enc[header.index(c)]
            trv = enc[header.index(c)]
            if isinstance(tv, str) and isinstance(trv, str):
                dist += 0.0 if tv == trv else 1.0
            elif isinstance(tv, float) and isinstance(trv, float):
                dist += abs(tv - trv) / 100.0

        if dist < best_dist:
            best_dist = dist
            best_match_idx = i

    predicted_goals = []
    for col in goals:
        v = float(train_enc[best_match_idx][header.index(col)])
        predicted_goals.append(v)

    n = len(rows)
    better_count = 0

    for i, r in enumerate(rows):
        if any(v == '?' for v in r):
            continue

        all_better = True
        for col in goals:
            actual = float(r[header.index(col)])
            pred = predicted_goals[goals.index(col)]
            if col.endswith('-'):
                # Lower is better (minimize)
                if pred <= actual:
                    continue
                else:
                    all_better = False
            else:
                # Higher is better (maximize)
                if pred >= actual:
                    continue
                else:
                    all_better = False

        if all_better:
            better_count += 1

    p = better_count / n
    reason = f"This setup beats {better_count} out of {n} other setups."

    return (p, reason)


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    test_row_idx = None
    for i, r in enumerate(rows):
        if any(v == '?' for v in r):
            test_row_idx = i
            break

    if test_row_idx is not None:
        p, reason = justify(header, rows, rows[test_row_idx])
        print(f"{p:.4f} - {reason}")
