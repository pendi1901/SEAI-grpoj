def blame(header, rows):
    """Return names of input columns that best explain why the worst rows are bad."""

    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]

    def to_float(cell):
        try:
            return float(cell)
        except (ValueError, TypeError):
            return 0.0

    # --- score every row on its goals ----------------------------------------
    goal_dirs = {}
    for c in goal_cols:
        goal_dirs[c] = 'min' if c.endswith('-') else 'max'

    n = len(rows)
    best_vals = []
    worst_vals = []
    for c in goal_cols:
        vals = [to_float(r[header.index(c)]) for r in rows]
        best_vals.append(min(vals))
        worst_vals.append(max(vals))

    row_scores = []
    for i, row in enumerate(rows):
        s = 0.0
        for j, c in enumerate(goal_cols):
            v = to_float(row[header.index(c)])
            if goal_dirs[c] == 'min':
                denom = best_vals[j] - worst_vals[j]
                if denom <= 0:
                    s += 1.0
                else:
                    s += (v - worst_vals[j]) / denom
            else:
                denom = best_vals[j] - worst_vals[j]
                if denom <= 0:
                    s += 1.0
                else:
                    s += (best_vals[j] - v) / denom
        row_scores.append(s / len(goal_cols))

    # --- split into worst ~5% vs the rest ------------------------------------
    k = max(1, int(n * 0.05))
    order = sorted(range(n), key=lambda i: row_scores[i], reverse=True)
    worst_indices = set(order[n - k:])
    best_indices = set(order[: n - k])

    # --- for each input column check if its value differs between groups -----
    is_numeric = [c[0].isupper() for c in header]
    result = []

    for i, col in enumerate(header):
        if not is_numeric[i]:
            continue
        if col in goal_cols:
            continue

        worst_vals_list = [to_float(rows[j][i]) for j in worst_indices]
        best_vals_list  = [to_float(rows[j][i]) for j in best_indices]

        mean_worst = sum(worst_vals_list) / len(worst_vals_list) if worst_vals_list else 0.0
        mean_best  = sum(best_vals_list)  / len(best_vals_list)  if best_vals_list  else 0.0

        all_vals = [to_float(rows[j][i]) for j in range(n)]
        overall_mean = sum(all_vals) / n
        overall_std = (sum((v - overall_mean) ** 2 for v in all_vals) / n) ** 0.5 if n > 1 else 0.0

        diff = abs(mean_worst - mean_best)
        if overall_std > 0 and diff > 0.3 * overall_std:
            result.append(col)

    return result


if __name__ == "__main__":
    import csv

    with open("Health-ClosedIssues0000.train.csv") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(10000)]

    bad_cols = blame(header, rows)
    print(f"Settings most responsible for the worst setups: {bad_cols}")
