def race(header, rows, label):
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    input_cols = [c for c in header if not c.endswith('-') and not c.endswith('+')]

    n = len(rows)

    def evaluate(i):
        goals = label(i)
        min_vals = {}
        max_vals = {}
        for col, val in zip(goal_cols, goals):
            v = float(val)
            if col not in min_vals or v < min_vals[col]:
                min_vals[col] = v
            if col not in max_vals or v > max_vals[col]:
                max_vals[col] = v
        score = 0.0
        for col, val in zip(goal_cols, goals):
            v = float(val)
            mn = min_vals[col]
            mx = max_vals[col]
            rng = (mx - mn) if mx > mn else 1.0
            norm = (v - mn) / rng
            if col.endswith('-'):
                score -= norm
            elif col.endswith('+'):
                score += norm
        return score

    def random_strategy():
        import random as _random
        indices = list(range(n))
        _random.shuffle(indices)
        chosen = indices[:50]
        best_idx = None
        best_score = float('-inf')
        for i in chosen:
            s = evaluate(i)
            if s > best_score:
                best_score = s
                best_idx = i
        return best_idx, best_score

    def scored_strategy():
        col_stats = {}
        for col in input_cols + goal_cols:
            vals = []
            for row in rows:
                v = row[header.index(col)]
                if v == '?':
                    continue
                try:
                    vals.append(float(v))
                except (ValueError, TypeError):
                    continue
            if len(vals) < 2:
                col_stats[col] = {'mean': 0.0, 'std': 1.0}
                continue
            mean_val = sum(vals) / len(vals)
            variance = sum((x - mean_val)**2 for x in vals) / (len(vals) - 1) if len(vals) > 1 else 0.0
            std_val = variance**0.5
            col_stats[col] = {'mean': mean_val, 'std': std_val}

        scores = []
        for i in range(n):
            s = 0.0
            for col in input_cols:
                v = float(rows[i][header.index(col)])
                stats = col_stats[col]
                if abs(stats['std']) < 1e-9:
                    s += (v - stats['mean']) / max(abs(stats['mean']), 1.0)
                else:
                    s += (v - stats['mean']) / stats['std']
            scores.append(s)

        indices = sorted(range(n), key=lambda i: scores[i], reverse=True)[:50]
        best_idx = None
        best_score = float('-inf')
        for i in indices:
            s = evaluate(i)
            if s > best_score:
                best_score = s
                best_idx = i
        return best_idx, best_score

    def flow_strategy():
        import random as _random
        seed = _random.randint(0, n - 1)
        current_goals = label(seed)
        min_vals = {}
        max_vals = {}
        for col, val in zip(goal_cols, current_goals):
            v = float(val)
            if col not in min_vals or v < min_vals[col]:
                min_vals[col] = v
            if col not in max_vals or v > max_vals[col]:
                max_vals[col] = v

        best_score = 0.0
        for col, val in zip(goal_cols, current_goals):
            v = float(val)
            mn = min_vals[col]
            mx = max_vals[col]
            rng = (mx - mn) if mx > mn else 1.0
            norm = (v - mn) / rng
            if col.endswith('-'):
                best_score -= norm
            elif col.endswith('+'):
                best_score += norm

        for _ in range(49):
            candidate_idx = _random.randint(0, n - 1)
            if candidate_idx == seed:
                continue
            cand_goals = label(candidate_idx)
            cand_min_vals = {}
            cand_max_vals = {}
            for col, val in zip(goal_cols, cand_goals):
                v = float(val)
                if col not in cand_min_vals or v < cand_min_vals[col]:
                    cand_min_vals[col] = v
                if col not in cand_max_vals or v > cand_max_vals[col]:
                    cand_max_vals[col] = v

            cand_score = 0.0
            for col, val in zip(goal_cols, cand_goals):
                v = float(val)
                mn = cand_min_vals[col]
                mx = cand_max_vals[col]
                rng = (mx - mn) if mx > mn else 1.0
                norm = (v - mn) / rng
                if col.endswith('-'):
                    cand_score -= norm
                elif col.endswith('+'):
                    cand_score += norm

            if cand_score >= best_score:
                seed = candidate_idx
                current_goals = cand_goals
                min_vals = cand_min_vals
                max_vals = cand_max_vals
                best_score = cand_score

        return seed, best_score

    results = {
        'random': random_strategy(),
        'scored': scored_strategy(),
        'flow': flow_strategy()
    }

    scores = [(name, score) for name, (idx, score) in results.items()]
    scores.sort(key=lambda x: x[1], reverse=True)

    winner_name = scores[0][0]
    winner_idx = results[winner_name][0]

    return {
        'winner': winner_name,
        'row': winner_idx,
        'tried': ['random', 'scored', 'flow']
    }


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('pom3a.train.csv')
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    goal_cols = [c for c in header if c.endswith('-')]
    test_rows = []
    for r in rows:
        if any(r[header.index(c)] == '?' for c in goal_cols):
            test_rows.append(r)

    if not test_rows:
        # All goals are numeric; simulate "?" by replacing with NaN
        import numpy as np
        for i, row in enumerate(rows):
            new_row = list(row)
            for col in goal_cols:
                idx = header.index(col)
                v = float(new_row[idx])
                if not np.isnan(v):
                    new_row[idx] = '?'
            test_rows.append(new_row)

    def make_label():
        goal_cols_list = [c for c in header if c.endswith('-')]
        original_rows = {i: list(row) for i, row in enumerate(rows)}

        def label(i):
            vals = []
            for col in goal_cols_list:
                v = float(original_rows[i][header.index(col)])
                vals.append(v)
            return vals

        return label

    label_fn = make_label()
    result = race(header, test_rows, label_fn)
    print(f"Winner: {result['winner']}, Row: {result['row']}")
