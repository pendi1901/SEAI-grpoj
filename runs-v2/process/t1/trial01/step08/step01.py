import csv


def remember(header, rows):
    goal_cols = ['Cost-', 'Score-', 'Idle-']

    # Parse valid rows (all three goals must be numeric)
    valid_rows = []  # list of (original_index, parsed_goals_dict)
    for i, row in enumerate(rows):
        ok = True
        goals = {}
        for col in goal_cols:
            idx = header.index(col)
            val = row[idx]
            if val == '?':
                ok = False
                break
            try:
                goals[col] = float(val)
            except ValueError:
                ok = False
                break
        if ok:
            valid_rows.append((i, goals))

    if not valid_rows:
        return []

    n = len(valid_rows)

    # Compute ranks for each goal among valid rows (lower value = better rank)
    goal_ranks = {col: {} for col in goal_cols}
    for col in goal_cols:
        vals = [(valid_rows[j][1][col], j) for j in range(n)]
        vals.sort(key=lambda x: x[0])
        for new_rank, (_, idx_in_valid) in enumerate(vals, 1):
            goal_ranks[col][idx_in_valid] = new_rank

    # Find rows that are top performers on ALL three goals simultaneously
    max_count = int(n * 0.05)
    threshold = n - max_count

    result = []
    for j, (orig_idx, goals) in enumerate(valid_rows):
        ranks = [goal_ranks[col][j] for col in goal_cols]
        if all(r <= threshold for r in ranks):
            result.append(orig_idx)

    return result


if __name__ == "__main__":
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    result = remember(header, rows)
    print(f"Found {len(result)} elite setups out of {len(rows)}:")
    for pos in sorted(result):
        c = float(rows[pos][header.index('Cost-')])
        s = float(rows[pos][header.index('Score-')])
        i = float(rows[pos][header.index('Idle-')])
        print(f"  Row {pos}: Cost-={c:.4f}, Score-={s:.4f}, Idle-={i:.4f}")
