def guess(header, train, test):
    goal_cols = ['Cost-', 'Score-', 'Idle-']

    def is_goal(col):
        return col.endswith('-') and col != '-'

    n_train = len(train)
    if n_train == 0:
        return [float('nan')] * len(test)

    # Stats for non-goal columns from training data.
    col_means = {}
    col_stds = {}
    for col in header:
        if not is_goal(col):
            vals = [float(row[header.index(col)]) for row in train]
            m = sum(vals) / len(vals)
            var = sum((v - m) ** 2 for v in vals) / len(vals)
            s = var ** 0.5
            col_means[col] = m
            col_stds[col] = s

    # Normalize Cost- from training data so 0 = best (lowest).
    cost_vals_train = [float(row[header.index('Cost-')]) for row in train]
    mn_cost, mx_cost = min(cost_vals_train), max(cost_vals_train)

    def norm_cost(v):
        if mx_cost == mn_cost:
            return 0.0
        return (v - mn_cost) / (mx_cost - mn_cost)

    cost_norm_train = [norm_cost(v) for v in cost_vals_train]

    # Correlations between non-goal columns and normalized Cost-.
    col_corrs = {}
    for col in header:
        if not is_goal(col):
            vals = [float(row[header.index(col)]) for row in train]
            n = len(vals)
            mx_v = sum(vals) / n
            mx_c = sum(cost_norm_train) / n
            num = sum((vals[i] - mx_v) * (cost_norm_train[i] - mx_c) for i in range(n))
            den_x = sum((v - mx_v) ** 2 for v in vals) ** 0.5
            den_y = sum((c - mx_c) ** 2 for c in cost_norm_train) ** 0.5
            col_corrs[col] = num / (den_x * den_y) if den_x != 0 and den_y != 0 else 0.0

    # Predict Cost- for each test row using the learned correlations.
    def predict(test_row):
        pred_norm = sum(
            col_corrs.get(col, 0.0) * (
                (float(test_row[header.index(col)]) - col_means[col]) / col_stds[col] if col_stds[col] != 0 else 0.0
            )
            for col in header if not is_goal(col)
        )
        return max(0.0, min(1.0, pred_norm))

    results = []
    for test_row in test:
        norm_pred = predict(test_row)
        cost_pred = mn_cost + norm_pred * (mx_cost - mn_cost) if mx_cost != mn_cost else 0.0
        results.append(cost_pred)

    return results


if __name__ == "__main__":
    import csv

    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [list(map(float, row)) for row in reader]

    result = guess(header, rows, rows[:1])  # predict Cost- for first training row using itself
    print(f"Predicted Cost- for sample: {result[0]:.4f}")
