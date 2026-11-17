import sys
sys.path.insert(0, '.')
from step01 import remember


def race(header, rows, label):
    goal_cols = [c for c in header if c.endswith('-')]
    input_cols = [c for c in header if not c.endswith('-')]

    n = len(rows)
    true_goals = {}
    for i in range(n):
        tg = []
        for col in goal_cols:
            tg.append(float(rows[i][header.index(col)]))
        true_goals[i] = tg

    # --- Strategy 1: remember (rank-based, uses full rows) ---
    def strat_remember():
        ref_rows = []
        for r in rows:
            new_r = list(r)
            for col in goal_cols:
                new_r[header.index(col)] = 0.0
            ref_rows.append(new_r)
        best_pos = remember(header, ref_rows)[0] if len(ref_rows) > 0 else None
        return best_pos

    # --- Strategy 2: choose (deviation from top-ranked input averages) ---
    def strat_choose():
        ref_rows = []
        for r in rows:
            new_r = list(r)
            for col in goal_cols:
                new_r[header.index(col)] = 0.0
            ref_rows.append(new_r)
        best_positions = remember(header, ref_rows)

        n_ref = len(ref_rows)
        col_means_top = {}
        for col in input_cols:
            vals_top = []
            vals_rest = []
            for i, r in enumerate(ref_rows):
                v = float(r[header.index(col)])
                if i in best_positions:
                    vals_top.append(v)
                else:
                    vals_rest.append(v)
            col_means_top[col] = (np.mean(vals_top), np.mean(vals_rest))

        best_pos = -1
        best_score = float('inf')
        for i in range(n):
            score = 0.0
            for col in input_cols:
                v = float(rows[i][header.index(col)])
                mean_top, _ = col_means_top[col]
                score += (v - mean_top) ** 2
            if score < best_score:
                best_score = score
                best_pos = i
        return best_pos

    # --- Strategy 3: random ---
    def strat_random():
        import random
        candidates = [i for i in range(n)]
        chosen = set()
        while len(chosen) < min(5, n):
            c = random.choice(candidates)
            chosen.add(c)
            candidates.remove(c)
        return list(chosen)[0]

    # --- Strategy 4: linear regression on inputs (from step02) ---
    from sklearn.linear_model import LinearRegression as LR
    X_train = np.array([[float(cell) for cell in row] for row in rows])
    y_train = np.array([true_goals[i][0] for i in range(n)])  # Cost-

    model = LR()
    model.fit(X_train, y_train)

    def strat_lr():
        preds = model.predict(X_train).tolist()
        return int(np.argmin(preds))

    # --- Strategy 5: multi-goal regression (all goals) ---
    y_all = np.array([true_goals[i] for i in range(n)])
    X_all = X_train
    from sklearn.linear_model import LinearRegression as LR2
    model2 = LR2()
    model2.fit(X_all, y_all)

    def strat_lr_multi():
        preds = model2.predict(X_all).tolist()
        # Sum of goals (lower is better for all '-' columns)
        return int(np.argmin(preds))

    strategies = [
        ("remember", strat_remember),
        ("choose", strat_choose),
        ("random", strat_random),
        ("lr_cost", strat_lr),
        ("lr_multi", strat_lr_multi),
    ]

    results = {}
    for name, fn in strategies:
        pos = fn()
        # Score this row by how close its true goals are to the best possible.
        tg = true_goals[pos]
        score = sum(tg)  # lower is better (all '-' columns)
        results[name] = (pos, score)

    # Pick the strategy with the lowest total goal score among those that tried at least one row.
    winner_name = min(results.keys(), key=lambda k: results[k][1])
    best_row = results[winner_name][0]

    return {
        "winner": winner_name,
        "row": best_row,
        "tried": [s[0] for s in strategies],
    }


if __name__ == "__main__":
    import pandas as pd
    import numpy as np

    df = pd.read_csv("pom3a.train.csv")
    header = list(df.columns)
    rows = [list(r) for _, r in df.iterrows()]

    goal_cols = [c for c in header if c.endswith('-')]
    for i, row in enumerate(rows):
        for col in goal_cols:
            row[header.index(col)] = '?'

    answer = race(header, rows, label=lambda i: None)  # label unused; true goals from original data
    print(f"Winner: {answer['winner']}, Row: {answer['row']}")
