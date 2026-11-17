import sys
sys.path.insert(0, ".")
from step01 import remember


def fix(header, row, levers):
    goal_cols = [h for h in header if h.endswith('-')]

    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    # Score a complete row based on goals: low is good for -cols, high for +cols
    def score(row_dict):
        s = 0.0
        for col in goal_cols:
            f = safe_float(row_dict[header.index(col)])
            if f is not None:
                if col.endswith('-'):
                    s -= f
                else:
                    s += f
        return s

    # Try all combinations of lever values and pick the one with best score.
    # Since goals are "?" in a bad row, we use training data patterns via remember().
    # We evaluate each candidate by checking if its lever values match any known-good setup.

    best_combo = {}
    best_score = float('-inf')

    def evaluate(combo):
        nonlocal best_combo, best_score
        test_row = dict(row)
        for col, val in combo.items():
            test_row[header.index(col)] = val
        s = score(test_row)
        if s > best_score:
            best_score = s
            best_combo = dict(combo)

    # Start with original row (no changes yet) — baseline
    evaluate({})

    for lever_col, allowed in levers.items():
        new_combos = []
        for existing in [best_combo]:  # extend from current best only? No — try all.
            pass
        # Actually we need to enumerate ALL combinations across all levers.
        # Simplest: build cartesian product of allowed values for each lever column.

    # Build full cartesian product of allowed values
    combo_keys = list(levers.keys())
    combo_values = [levers[k] for k in combo_keys]

    def cartesian_product(values_list):
        if not values_list:
            return [[]]
        rest = cartesian_product(values_list[1:])
        return [[v] + r for v, r in zip(values_list[0], rest)]

    all_combos = cartesian_product(combo_values)

    for combo in all_combos:
        evaluate(dict(zip(combo_keys, combo)))

    # Apply best changes to row and return them
    result = {}
    for col, val in best_combo.items():
        result[col] = val

    return result


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("pom3a.train.csv")
    header = list(df.columns)
    rows = []
    for _, row in df.iterrows():
        r = []
        for col in header:
            val = row[col]
            if pd.isna(val):
                r.append("?")
            else:
                r.append(float(val))
        rows.append(r)

    # Pick a bad row (high Cost- and Idle-)
    goal_cols = [h for h in header if h.endswith('-')]
    def row_score(row):
        s = 0.0
        for col in goal_cols:
            try:
                f = float(row[header.index(col)])
                if col.endswith('-'):
                    s -= f
                else:
                    s += f
            except (ValueError, TypeError):
                continue
        return s

    bad_rows = [r for r in rows if "?" not in r]
    worst_idx = sorted(range(len(bad_rows)), key=lambda i: row_score(bad_rows[i]))[:5]

    print("Worst setups:")
    for idx in worst_idx:
        c, i = (bad_rows[idx][header.index(c)] for c in ['Cost-', 'Idle-'])
        print(f"  Row {idx}: Cost-={c:.4f}, Idle-={i:.4f}")

    # Show what fix() would do on the worst row
    levers_example = {}
    for col in ['Team Size', 'Plan']:
        if col in header:
            idx = header.index(col)
            val = bad_rows[worst_idx[0]][idx]
            if "?" not in (val,):
                levers_example[col] = [val - 0.1, val + 0.1]

    print(f"\nExample fix on worst row:")
    result = fix(header, bad_rows[worst_idx[0]], levers_example)
    print(f"  Changes: {result}")
