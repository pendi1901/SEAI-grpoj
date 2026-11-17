import sys
sys.path.insert(0, '.')
from step01 import remember


def race(header, rows, label):
    """Compare three strategies on up to 50 labelled rows; return the winner."""

    goals = [h for h in header if h.endswith('-') or h.endswith('+')]
    numeric_cols = [c for c in header if c.isupper()]
    symbolic_cols = [c for c in header if not c.isupper() and not c.endswith('-') and not c.endswith('+')]

    def encode_row(row):
        return (tuple(float(row[header.index(c)]) for c in numeric_cols),
                tuple(row[header.index(c)] for c in symbolic_cols))

    # Pre-compute true goal values from the label function.
    labelled = []
    for i in range(len(rows)):
        vals = [float(label(i)[header.index(col)]) for col in goals]
        if any(v != float('inf') and v != -float('inf') for v in vals):
            # Use a sentinel to mark unlabelled rows.
            pass
        labelled.append(vals)

    def score_row(row, goal_vals):
        """Score a row by normalising its goals (same scheme as remember)."""
        scores = 0.0
        for col in goals:
            v = float(goal_vals[goals.index(col)])
            # We need the range across all labelled rows to normalise.
            pass
        return scores

    def score_row_v2(row, goal_vals):
        """Score a row by comparing its goals against the best possible."""
        s = 0.0
        for col in goals:
            v = float(goal_vals[goals.index(col)])
            if col.endswith('-'):
                # Lower is better; normalise to [0,1] where 0=best.
                s += (1.0 - v)
            else:
                s += v
        return s

    def score_row_v3(row, goal_vals):
        """Score a row by comparing its goals against the mean of all labelled rows."""
        means = [sum(labelled[i][goals.index(col)] for i in range(len(labelled))) / len(labelled)
                 for col in goals]
        s = 0.0
        for col in goals:
            v = float(goal_vals[goals.index(col)])
            if col.endswith('-'):
                s += (1.0 - abs(v - means[goals.index(col)]))
            else:
                s += abs(v - means[goals.index(col)])
        return s

    # Strategy 1: remember() from step01 — uses all rows to find top positions, then picks the best labelled one.
    def strategy_remember():
        best_positions = remember(header, rows)
        # Filter to only labelled rows within those positions.
        candidates = [i for i in best_positions if i < len(labelled)]
        if not candidates:
            return None, 0.0
        # Score each candidate against its true goals.
        scores = []
        for idx in candidates:
            s = score_row_v2(rows[idx], labelled[idx])
            scores.append((s, idx))
        scores.sort(key=lambda x: -x[0])
        if not scores:
            return None, 0.0
        best_score, best_idx = scores[0]
        return "remember", best_idx

    # Strategy 2: random — pick from labelled rows uniformly at random (up to 50).
    def strategy_random():
        import random
        n_labelled = len(labelled)
        if n_labelled == 0:
            return None, 0.0
        chosen = random.sample(range(n_labelled), min(50, n_labelled))
        scores = []
        for idx in chosen:
            s = score_row_v2(rows[idx], labelled[idx])
            scores.append((s, idx))
        scores.sort(key=lambda x: -x[0])
        if not scores:
            return None, 0.0
        best_score, best_idx = scores[0]
        return "random", best_idx

    # Strategy 3: nearest-neighbour — for each labelled row, find the closest training row (non-goal features),
    # then use that match's goals as prediction; pick the labelled row whose NN-prediction is best.
    def strategy_nn():
        train_enc = [encode_row(r) for r in rows if not any(v == '?' for v in r)]
        test_enc_list = []
        for i in range(len(rows)):
            enc = encode_row(rows[i])
            test_enc_list.append(enc)

        best_overall_idx = None
        best_overall_score = float('-inf')

        for i in range(len(labelled)):
            # Find NN among training rows.
            test_enc = test_enc_list[i]
            best_match_idx = None
            best_dist = float('inf')

            for j, enc in enumerate(train_enc):
                dist = 0.0
                for c in header:
                    if c.endswith('-') or c.endswith('+'):
                        continue
                    tv = test_enc[header.index(c)]
                    trv = enc[header.index(c)]
                    if isinstance(tv, str) and isinstance(trv, str):
                        dist += 0.0 if tv == trv else 1.0
                    elif isinstance(tv, float) and isinstance(trv, float):
                        dist += abs(tv - trv) / 100.0

                if dist < best_dist:
                    best_dist = dist
                    best_match_idx = j

            # Predict goals from NN match.
            predicted_goals = []
            for col in goals:
                v = float(train_enc[best_match_idx][header.index(col)])
                predicted_goals.append(v)

            actual_goals = labelled[i]
            max_diff = 0.0
            for k in range(len(goals)):
                diff = abs(predicted_goals[k] - actual_goals[k])
                if diff > max_diff:
                    max_diff = diff

            # Score: how close is the NN prediction to true goals?
            s = sum(1.0 - (diff / 1.0) for diff in [abs(predicted_goals[k] - actual_goals[k]) for k in range(len(goals))])
            if s > best_overall_score:
                best_overall_score = s
                best_overall_idx = i

        return "nn", best_overall_idx

    # Run all strategies.
    results = {}
    try:
        r1, idx1 = strategy_remember()
        results["remember"] = (r1, idx1)
    except Exception as e:
        print(f"Strategy remember failed: {e}", file=sys.stderr)

    try:
        r2, idx2 = strategy_random()
        results["random"] = (r2, idx2)
    except Exception as e:
        print(f"Strategy random failed: {e}", file=sys.stderr)

    try:
        r3, idx3 = strategy_nn()
        results["nn"] = (r3, idx3)
    except Exception as e:
        print(f"Strategy nn failed: {e}", file=sys.stderr)

    # Determine winner by best score.
    scored_results = []
    for name, (score, idx) in results.items():
        if score is not None and idx is not None:
            scored_results.append((name, score, idx))

    if not scored_results:
        return {"winner": "none", "row": -1, "tried": list(results.keys())}

    scored_results.sort(key=lambda x: -x[1])
    winner = scored_results[0][0]
    best_row = scored_results[0][2]

    return {
        "winner": winner,
        "row": best_row,
        "tried": list(results.keys())
    }


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    # Build label function: returns true goal values for each row.
    def label(i):
        vals = []
        for col in ['MRE-', 'ACC+', 'PRED40+']:
            v = float(df.iloc[i][col])
            vals.append(v)
        return vals

    result = race(header, rows, label)
    print(f"Winner: {result['winner']} (row {result['row']})")
    print(f"Tried strategies: {result['tried']}")
