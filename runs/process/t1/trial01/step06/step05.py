import csv
import math


def blame(header, rows):
    """Identify input columns that explain why the worst setups are bad."""

    goals = [c for c in header if c.endswith('-')]
    inputs = [c for c in header if not c.endswith('-')]

    n = len(rows)

    # Compute total normalized score per row (lower is better)
    goal_mins = {}
    goal_maxs = {}
    for g in goals:
        vals = []
        for r in rows:
            v = float(r[header.index(g)])
            vals.append(v)
        goal_mins[g] = min(vals)
        goal_maxs[g] = max(vals)

    scores = []
    for i, r in enumerate(rows):
        total = 0.0
        for g in goals:
            v = float(r[header.index(g)])
            if goal_maxs[g] == goal_mins[g]:
                norm = 0.0
            else:
                norm = (v - goal_mins[g]) / (goal_maxs[g] - goal_mins[g])
            total += norm
        scores.append((total, i))

    # Sort descending so worst rows come first
    scores.sort(reverse=True)

    k = max(1, n // 5)
    worst_indices = sorted([pos for _, pos in scores[:k]])
    best_indices = sorted([pos for _, pos in scores[-k:]])

    result = []
    for col in inputs:
        worst_vals = [float(r[header.index(col)]) for i, r in enumerate(rows) if i in worst_indices]
        best_vals = [float(r[header.index(col)]) for i, r in enumerate(rows) if i in best_indices]

        if not worst_vals or not best_vals:
            continue

        mean_worst = sum(worst_vals) / len(worst_vals)
        mean_best = sum(best_vals) / len(best_vals)

        var_w = sum((v - mean_worst) ** 2 for v in worst_vals) / max(len(worst_vals) - 1, 1) if len(worst_vals) > 1 else 0.0
        var_b = sum((v - mean_best) ** 2 for v in best_vals) / max(len(best_vals) - 1, 1) if len(best_vals) > 1 else 0.0

        se = math.sqrt(var_w / len(worst_vals) + var_b / len(best_vals))
        if se == 0:
            continue

        t_stat = abs(mean_worst - mean_best) / se

        # Significant difference means this column explains badness
        if t_stat > 2.0:
            direction = "high" if mean_worst > mean_best else "low"
            result.append(f"{col} tends to be {direction} in bad setups")

    return result


if __name__ == "__main__":
    with open('pom3a.train.csv', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            if len(row) == len(header):
                rows.append(row)

    reasons = blame(header, rows)
    print("Why the worst setups are bad:")
    for r in reasons:
        print(f"  - {r}")
