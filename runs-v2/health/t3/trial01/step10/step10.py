import pandas as pd
import numpy as np


def race(header, rows, label):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if not c.endswith('-') and not c.endswith('+')]

    n_rows = len(rows)

    # --- helper: score a row from its real goals ---
    def real_score(row):
        s = 0.0
        for col in goal_cols:
            v = float(row[header.index(col)])
            span = best[col] - worst[col]
            if span > 1e-9:
                normed = (v - worst[col]) / span
            else:
                normed = 0.5
            s += normed
        return s

    # --- helper: score a row from predicted goals (linear model) ---
    def pred_score(row):
        x = [float(row[input_cols.index(c)]) for c in input_cols]
        pred_goals = {}
        for col, m in models.items():
            pred_goals[col] = float(m.predict([x])[0])
        s = 0.0
        for col in goal_cols:
            v = pred_goals[col]
            span = best[col] - worst[col]
            if span > 1e-9:
                normed = (v - worst[col]) / span
            else:
                normed = 0.5
            s += normed
        return s

    # --- build training data from clean rows ---
    X_train = []
    y_goals = {}
    for i, row in enumerate(rows):
        has_q = False
        for col in goal_cols:
            if row[header.index(col)] == '?':
                has_q = True
                break
        if not has_q:
            x = [float(row[input_cols.index(c)]) for c in input_cols]
            X_train.append(x)
            for col in goal_cols:
                y_goals.setdefault(col, []).append(float(row[header.index(col)]))

    X_train = np.array(X_train) if X_train else np.empty((0, len(input_cols)))
    models = {}
    for col, vals in y_goals.items():
        m = LinearRegression()
        m.fit(X_train, np.array(vals))
        models[col] = m

    # --- compute best/worst per goal from clean rows ---
    best = {}
    worst = {}
    for col in goal_cols:
        vals = y_goals.get(col, [])
        if not vals:
            continue
        if col.endswith('-'):
            best[col], worst[col] = min(vals), max(vals)
        else:
            best[col], worst[col] = max(vals), min(vals)

    # --- Strategy 1: random (pick rows at random, up to 50) ---
    rng = np.random.default_rng(42)
    n_random = min(50, n_rows)
    random_indices = sorted(rng.choice(n_rows, size=n_random, replace=False).tolist())

    # --- Strategy 2: greedy hill-climb (pick best unseen row each step, up to 50) ---
    remaining = list(range(n_rows))
    chosen_greedy = []
    for _ in range(min(50, n_rows)):
        if not remaining:
            break
        # score each remaining row using real goals (or predicted if dirty)
        best_s = -np.inf
        best_i = None
        for i in remaining:
            s = real_score(rows[i]) if label(i) else pred_score(rows[i])
            if s > best_s + 1e-9:
                best_s = s
                best_i = i
        chosen_greedy.append(best_i)
        remaining.remove(best_i)

    # --- Strategy 3: linear-regression predictor (pick top-k by predicted score, then verify with real label if available) ---
    scores_pred = [pred_score(rows[i]) for i in range(n_rows)]
    top_k = min(50, n_rows)
    pred_order = np.argsort(scores_pred)[::-1][:top_k].tolist()

    # --- pick the best row overall from each strategy's chosen set ---
    def find_best_in(indices):
        if not indices:
            return None, -np.inf
        best_s = -np.inf
        best_i = None
        for i in indices:
            s = real_score(rows[i]) if label(i) else pred_score(rows[i])
            if s > best_s + 1e-9:
                best_s = s
                best_i = i
        return best_i, best_s

    r_random, s_random = find_best_in(random_indices)
    r_greedy, s_greedy = find_best_in(chosen_greedy)
    r_pred, s_pred = find_best_in(pred_order)

    # --- pick the overall winner ---
    candidates = [
        ("random", r_random),
        ("greedy", r_greedy),
        ("predictor", r_pred),
    ]
    best_name = None
    best_row = None
    for name, idx in candidates:
        if idx is not None and (best_name is None or s_real(idx) > s_real(best_row)):
            best_name = name
            best_row = idx

    return {
        "winner": best_name,
        "row": best_row,
        "tried": ["random", "greedy", "predictor"],
    }


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(r) for r in df.values]

    result = race(header, rows, label)
    print(f"Winner: {result['winner']}  Row #{result['row'] + 1}  Tried: {result['tried']}")
