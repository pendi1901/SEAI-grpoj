def flow(header, row, seen):
    goal_cols = [c for c in header if c.endswith('-')]

    def parse_goals(row_dict):
        vals = []
        for col in goal_cols:
            v = row_dict[header.index(col)]
            try:
                vals.append(float(v))
            except (ValueError, TypeError):
                return None
        return vals

    current = parse_goals(row)
    if current is None:
        return False

    if not seen:
        return True

    best = {}
    for s in seen:
        sg = parse_goals(s)
        if sg is None:
            continue
        for col, val in zip(goal_cols, sg):
            if col not in best or val < best[col]:
                best[col] = val

    for i, col in enumerate(goal_cols):
        if current[i] > best[col]:
            return False

    return True


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    chosen_idx = 0
    seen = []
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            chosen_idx = i
            break
        seen.append(row)

    print(
        f"Approved proposal #{chosen_idx + 1} "
        f"(Cost-={rows[chosen_idx][header.index('Cost-')]:.4f}, "
        f"Score-={rows[chosen_idx][header.index('Score-')]:.4f}, "
        f"Idle-={rows[chosen_idx][header.index('Idle-')]:.4f})"
    )
