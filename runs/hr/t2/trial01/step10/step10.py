import csv


def remember(header, rows):
    goal_cols = [c for c in header if c.endswith('+')]

    best_positions = []
    for i, row in enumerate(rows):
        score = 0
        valid = True
        for col in goal_cols:
            val = row[header.index(col)]
            if val == '?':
                valid = False
                break
            try:
                score += float(val)
            except ValueError:
                valid = False
                break
        if not valid:
            continue
        best_positions.append((score, i))

    best_positions.sort(reverse=True)

    max_count = max(1, int(len(rows) * 0.05))
    return [int(pos) for _, pos in best_positions[:max_count]]


def blame(header, rows):
    goal_cols = [c for c in header if c.endswith('+')]
    feature_cols = [c for c in header if not c.endswith('+') and c != 'attrition']

    scores = []
    for row in rows:
        s = 0.0
        valid = True
        for col in goal_cols:
            val = row[header.index(col)]
            try:
                s += float(val)
            except ValueError:
                valid = False
                break
        if not valid:
            continue
        scores.append((s, row))

    scores.sort()

    n_worst = max(1, len(scores) // 5)
    worst_rows = [row for _, row in scores[:n_worst]]

    result = []
    for col in feature_cols:
        vals = [float(row[header.index(col)]) for row in rows]
        n = len(vals)
        mean_v = sum(vals) / n
        mean_s = sum(s for s, _ in scores) / len(scores) if scores else 0.0

        num = sum((vals[i] - mean_v) * (scores[i][0] - mean_s) for i in range(n))
        den_x = sum((v - mean_v) ** 2 for v in vals) ** 0.5
        den_y = sum((s - mean_s) ** 2 for s, _ in scores) ** 0.5

        if den_x > 1e-10 and den_y > 1e-10:
            corr = num / (den_x * den_y)
        else:
            corr = 0.0

        result.append((abs(corr), col))

    result.sort(reverse=True)

    return [col for _, col in result[:5]]


def justify(header, rows, row):
    goal_cols = [c for c in header if c.endswith('+')]
    feature_cols = [c for c in header if not c.endswith('+') and c != 'attrition']

    X_train = []
    Y_train = []
    for r in rows:
        x_row = [float(r[header.index(c)]) for c in feature_cols]
        y_val = float(r[header.index(goal_cols[0])])
        X_train.append(x_row)
        Y_train.append(y_val)

    n = len(Y_train)
    p = len(X_train[0])
    mean_x = [sum(row[j] for row in X_train) / n for j in range(p)]
    mean_y = sum(Y_train) / n

    lam = 0.01
    XtX = [[0.0]*p for _ in range(p)]
    for j in range(p):
        for k in range(j, p):
            s = sum(X_train[i][j] * X_train[i][k] for i in range(n))
            if j == k:
                XtX[j][k] += lam
            else:
                XtX[j][k] *= 2

    Xty = [sum(X_train[i][j] * Y_train[i] for i in range(n)) for j in range(p)]
    aug = [list(row) + [Xty[j]] for j, row in enumerate(XtX)]
    for col in range(p):
        if abs(aug[col][col]) < 1e-10:
            continue
        for row_idx in range(col+1, p):
            factor = aug[row_idx][col] / aug[col][col]
            for k in range(col, p+1):
                aug[row_idx][k] -= factor * aug[col][k]

    weights = [aug[i][p] / aug[i][i] if abs(aug[i][i]) > 1e-10 else 0.0 for i in range(p)]

    x_test = [float(row[header.index(c)]) for c in feature_cols]
    pred = sum(weights[j] * (x_test[j] - mean_x[j]) for j in range(len(weights))) + mean_y

    p_count = 0.0
    for r in rows:
        x_row = [float(r[header.index(c)]) for c in feature_cols]
        pred_r = sum(weights[j] * (x_row[j] - mean_x[j]) for j in range(len(weights))) + mean_y
        if pred_r < pred:
            p_count += 1.0

    fraction = p_count / len(rows)

    reason = f"This employee ranks better than {fraction:.0%} of others based on tenure predictors."
    return (fraction, reason)


def choose(header, rows, label):
    goal_cols = [c for c in header if c.endswith('+')]
    feature_cols = [c for c in header if not c.endswith('+') and c != 'attrition']

    n = len(rows)
    p = len(feature_cols)

    mean_x = []
    for j in range(p):
        col_name = feature_cols[j]
        vals = [float(row[header.index(col_name)]) for row in rows]
        mean_x.append(sum(vals) / n)

    scores = []
    for i, row in enumerate(rows):
        s = 0.0
        for j in range(p):
            col_name = feature_cols[j]
            val = float(row[header.index(col_name)]) - mean_x[j]
            s += val
        scores.append((s, i))

    max_candidates = min(50, n)
    scores.sort(reverse=True)
    candidate_indices = [i for _, i in scores[:max_candidates]]

    best_score = -1e9
    best_idx = -1

    for idx in candidate_indices:
        true_goals = label(idx)
        if not true_goals or len(true_goals) != len(goal_cols):
            continue

        goal_score = sum(true_goals)
        if goal_score > best_score:
            best_score = goal_score
            best_idx = idx

    return best_idx


def race(header, rows, label):
    strategies = ['remember', 'blame', 'justify', 'choose', 'random']

    tried = []
    results = {}

    for strat in strategies:
        if strat == 'random':
            import random
            idx = random.randint(0, len(rows) - 1)
        elif strat == 'remember':
            from step01 import remember as _remember
            idx = _remember(header, rows)[0]
        elif strat == 'blame':
            from step05 import blame as _blame
            cols = _blame(header, rows)
            goal_cols = [c for c in header if c.endswith('+')]
            feature_cols = [c for c in header if not c.endswith('+') and c != 'attrition']

            scores = []
            for row in rows:
                s = 0.0
                valid = True
                for col in goal_cols:
                    val = row[header.index(col)]
                    try:
                        s += float(val)
                    except ValueError:
                        valid = False
                        break
                if not valid:
                    continue
                scores.append((s, row))

            scores.sort()
            n_worst = max(1, len(scores) // 5)
            worst_rows = [row for _, row in scores[:n_worst]]

            best_corr_col = cols[0] if cols else feature_cols[0]
            vals = [float(row[header.index(best_corr_col)]) for row in rows]
            mean_v = sum(vals) / len(vals)
            idx = max(range(len(rows)), key=lambda i: abs(float(rows[i][header.index(best_corr_col)]) - mean_v))

        elif strat == 'justify':
            from step06 import justify as _justify
            idx = _justify(header, rows, rows[0])[1]

        elif strat == 'choose':
            from step07 import choose as _choose
            goal_cols = [c for c in header if c.endswith('+')]
            idx = _choose(header, rows, lambda i: [float(rows[i][header.index(c)]) for c in goal_cols])

        tried.append(strat)
        true_goals = label(idx)
        results[strat] = (idx, true_goals)

    best_strat = max(results.keys(), key=lambda s: sum(results[s][1]))
    return {
        'winner': best_strat,
        'row': results[best_strat][0],
        'tried': tried
    }


if __name__ == "__main__":
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    result = race(header, rows, lambda i: [float(rows[i][header.index(c)]) for c in [c for c in header if c.endswith('+')]])
    print(f"Winner strategy: {result['winner']}, best row at position {result['row']}")
