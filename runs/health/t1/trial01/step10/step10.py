def race(header, rows, label):
    """Compare three strategies for finding the best row among up to 50 candidates."""

    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    is_numeric = [c[0].isupper() for c in header]

    def to_float(cell):
        try:
            return float(cell)
        except (ValueError, TypeError):
            return 0.0

    # --- helpers ---------------------------------------------------------------
    goal_dirs = {}
    for c in goal_cols:
        goal_dirs[c] = 'min' if c.endswith('-') else 'max'

    def score_row(row):
        """Score a row on its goals (numeric NN estimate when cell is '?')."""
        s = 0.0
        n_goals = len(goal_cols)
        for j, gcol in enumerate(goal_cols):
            v = to_float(row[header.index(gcol)])
            if gcol.endswith('-'):
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
        return s / n_goals

    # Precompute best/worst per goal column from training data
    best_vals = []
    worst_vals = []
    for gcol in goal_cols:
        vals = [to_float(r[header.index(gcol)]) for r in rows]
        best_vals.append(min(vals))
        worst_vals.append(max(vals))

    # --- strategy 1: random ---------------------------------------------------
    def strategy_random():
        import random
        rng = random.Random(0)
        candidates = list(range(len(rows)))
        rng.shuffle(candidates)
        chosen = []
        for i in candidates:
            if label(i) is not None:
                chosen.append(i)
            if len(chosen) >= 50:
                break
        return chosen

    # --- strategy 2: nearest-neighbour to best known good ----------------------
    def strategy_nn():
        """Pick rows whose non-goal numeric values are close to the row with the best score."""
        # Find the training row that has the best score (using its true goal values)
        best_row = None
        best_score = -1e9
        for i, row in enumerate(rows):
            if label(i) is not None:
                s = 0.0
                n_goals = len(goal_cols)
                for j, gcol in enumerate(goal_cols):
                    v = to_float(row[header.index(gcol)])
                    if gcol.endswith('-'):
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
                s /= n_goals
                if s > best_score:
                    best_score = s
                    best_row = row

        if best_row is None:
            return []

        # Now pick rows whose non-goal numeric values are closest to best_row's
        candidates = []
        for i, row in enumerate(rows):
            if label(i) is not None and i != best_row.__class__ if hasattr(best_row, '__class__') else False:
                pass  # placeholder; we'll just collect all labelled rows

        # Simpler: pick the first 50 labelled rows whose non-goal numeric distance to best_row is small
        candidates = []
        for i in range(len(rows)):
            if label(i) is not None:
                dist = 0.0
                for j in range(len(header)):
                    if not is_numeric[j]:
                        continue
                    if j == header.index(goal_cols[0]):  # skip first goal; we'll skip all goals
                        continue
                    bv = to_float(best_row[j])
                    rv = to_float(row[j])
                    diff = bv - rv
                    dist += diff * diff
                candidates.append((dist, i))

        candidates.sort(key=lambda x: x[0])
        chosen = [i for _, i in candidates[:50]]
        return chosen

    # --- strategy 3: random but seeded differently -----------------------------
    def strategy_random2():
        import random
        rng = random.Random(42)
        candidates = list(range(len(rows)))
        rng.shuffle(candidates)
        chosen = []
        for i in candidates:
            if label(i) is not None:
                chosen.append(i)
            if len(chosen) >= 50:
                break
        return chosen

    # --- run strategies -------------------------------------------------------
    tried = ["random", "nn", "random2"]
    results = {}
    for name in tried:
        fn = {"random": strategy_random, "nn": strategy_nn, "random2": strategy_random2}[name]
        row_indices = fn()
        # Score each chosen row using its true goal values (via label)
        scores = []
        for i in row_indices:
            s = 0.0
            n_goals = len(goal_cols)
            for j, gcol in enumerate(goal_cols):
                v = to_float(rows[i][header.index(gcol)])
                if gcol.endswith('-'):
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
            scores.append(s / n_goals)

        # Pick the row with highest score among chosen
        best_idx = max(range(len(scores)), key=lambda k: scores[k])
        results[name] = {"row": row_indices[best_idx], "score": scores[best_idx]}

    # Determine winner (highest score)
    winner_name = max(results, key=lambda n: results[n]["score"])
    return {
        "winner": winner_name,
        "row": results[winner_name]["row"],
        "tried": tried,
    }


if __name__ == "__main__":
    import csv

    with open("Health-ClosedIssues0000.train.csv") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(10000)]

    # Replace goal cells with "?" to simulate hidden goals
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    goal_indices = [header.index(c) for c in goal_cols]
    for row in rows:
        for idx in goal_indices:
            row[idx] = "?"

    # Define label function: returns true goal values for first 50 rows (or all labelled)
    def label(i):
        if i < 50:
            return [to_float(rows[i][header.index(c)]) for c in goal_cols]
        return None

    result = race(header, rows, label)
    print(f"Winner: {result['winner']} (row index {result['row']}, score={result.get('score', 0):.4f})")
