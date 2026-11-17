import csv


def guess(header, train, test):
    goals_min = [c for c in header if c.endswith('-')]
    goals_max = [c for c in header if c.endswith('+')]

    # Build a simple linear model: predict each goal column from all numeric inputs.
    # We use only the non-goal columns as features (symbolic + numeric).
    feature_cols = []
    for c in header:
        if c not in goals_min and c not in goals_max:
            feature_cols.append(c)

    n_train = len(train)
    n_features = len(feature_cols)

    # Collect training data per goal column.
    train_data = {c: [] for c in goals_min + goals_max}
    for row in train:
        feats = [float(row[c]) if c in feature_cols else 0.0 for c in feature_cols]
        for g in goals_min:
            train_data[g].append((feats, float(row[g])))
        for g in goals_max:
            train_data[g].append((feats, float(row[g])))

    # Fit a simple linear regression per goal using normal equations.
    # y = X @ w + b  ->  minimize sum((y - Xw - b)^2)
    def fit_linear(data):
        n = len(data)
        if n == 0:
            return [0.0] * n_features, 0.0

        # Compute sums for normal equations: (X^T X + reg*I) w = X^T y
        reg = 1e-6
        XtX = [[reg] * n_features for _ in range(n_features)]
        Xty = [0.0] * n_features
        sum_y = 0.0

        for feats, y in data:
            sum_y += y
            for j in range(n_features):
                xj = feats[j] if j < len(feats) else 0.0
                Xty[j] += xj * y
                for i in range(j + 1):
                    Xi = feats[i] if i < len(feats) else 0.0
                    XtX[i][j] += xj * Xi

        # Solve using Gaussian elimination with partial pivoting.
        m = n_features
        aug = [XtX[i][:] + [Xty[i]] for i in range(m)]
        for col in range(m):
            max_row = col
            for row in range(col + 1, m):
                if abs(aug[row][col]) > abs(aug[max_row][col]):
                    max_row = row
            aug[col], aug[max_row] = aug[max_row], aug[col]
            pivot = aug[col][col]
            if abs(pivot) < 1e-12:
                continue
            for row in range(col + 1, m):
                factor = aug[row][col] / pivot
                for k in range(col, m + 1):
                    aug[row][k] -= factor * aug[col][k]

        w = [0.0] * m
        b = sum_y / n if n > 0 else 0.0
        for i in range(m - 1, -1, -1):
            s = aug[i][m]
            for j in range(i + 1, m):
                s -= aug[i][j] * w[j]
            if abs(aug[i][i]) < 1e-12:
                w[i] = 0.0
            else:
                w[i] = s / aug[i][i]

        return w, b

    models = {}
    for g in goals_min + goals_max:
        w, b = fit_linear(train_data[g])
        models[g] = (w, b)

    # Predict first goal column for each test row.
    results = []
    for row in test:
        feats = [float(row[c]) if c in feature_cols else 0.0 for c in feature_cols]
        g = goals_min[0]  # first goal column
        w, b = models[g]
        pred = sum(w[j] * feats[j] for j in range(len(feats))) + b
        results.append(pred)

    return results


if __name__ == "__main__":
    import csv

    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        train = [next(reader) for _ in range(1470)]

    # Create a synthetic test row (day-one new hire, goals hidden).
    test_row = ["?"] * len(header)
    results = guess(header, train, [test_row])
    print(f"Estimated stay ({results[0]:.2f}) for the newly hired employee.")
