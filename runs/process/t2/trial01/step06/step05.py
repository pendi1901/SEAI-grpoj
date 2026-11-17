def blame(header, rows):
    goal_cols = ['Cost-', 'Score-', 'Idle-']

    def is_goal(col):
        return col.endswith('-') and col != '-'

    n = len(rows)
    if n == 0:
        return []

    # Normalise each goal column to [0,1] where 0 is best (lowest value).
    min_vals = {}
    max_vals = {}
    for col in goal_cols:
        vals = [float(row[header.index(col)]) for row in rows]
        mn, mx = min(vals), max(vals)
        if mx == mn:
            min_vals[col], max_vals[col] = 0.0, 1.0
        else:
            min_vals[col], max_vals[col] = mn, mx

    # Combined normalised badness per row (higher is worse).
    badnesses = []
    for row in rows:
        b = sum(
            (float(row[header.index(col)]) - min_vals[col]) / (max_vals[col] - min_vals[col])
            for col in goal_cols
        )
        badnesses.append(b)

    # For each non-goal column, compute Pearson correlation with overall badness.
    col_corrs = {}
    mean_badness = sum(badnesses) / n
    var_badness = sum((b - mean_badness) ** 2 for b in badnesses) ** 0.5

    for col in header:
        if not is_goal(col):
            vals = [float(row[header.index(col)]) for row in rows]
            mx_v = sum(vals) / n
            var_x = sum((v - mx_v) ** 2 for v in vals) ** 0.5
            col_corrs[col] = (sum(
                (vals[i] - mx_v) * (badnesses[i] - mean_badness) for i in range(n)
            ) / (var_x * var_badness)) if var_x != 0 and var_badness != 0 else 0.0

    # Rank by absolute correlation — strongest predictors of bad outcomes first.
    ranked = sorted(col_corrs.items(), key=lambda x: -abs(x[1]))
    return [col for col, _ in ranked[:5]]


if __name__ == "__main__":
    import csv

    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [list(map(float, row)) for row in reader]

    result = blame(header, rows)
    print("The worst setups are most associated with:")
    for col in result:
        print(f"  {col}")
