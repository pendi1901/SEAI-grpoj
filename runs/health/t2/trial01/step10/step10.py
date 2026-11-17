from step09 import spot


def race(header, rows, label):
    """Compare three strategies; return dict with winner info."""

    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]

    # Identify numeric input columns (uppercase, not goals)
    input_cols = []
    for col in header:
        if col[0].isupper() and col not in goal_cols:
            input_cols.append(col)

    target_col = goal_cols[0]  # "MRE-"

    def score_row(row):
        """Normalised score (higher is better)."""
        s = 0.0
        for col in goal_cols:
            vals = []
            for r in rows:
                try:
                    v = float(r[header.index(col)])
                    vals.append(v)
                except ValueError:
                    pass
            if not vals:
                continue
            mn, mx = min(vals), max(vals)
            try:
                v = float(row[header.index(col)])
            except ValueError:
                return -1e9
            if col.endswith('-'):
                s += (mx - v) / (mx - mn + 1e-9)
            else:
                s += (v - mn) / (mx - mn + 1e-9)
        return s

    def knn_predict(row):
        """Predict MRE using KNN on input columns."""
        inputs_new = [float(row[col]) for col in input_cols]
        train_data = []
        for r in rows:
            inputs = [float(r[c]) for c in input_cols]
            try:
                mre = float(r[target_col])
            except ValueError:
                continue
            train_data.append((inputs, mre))

        if not train_data:
            return 0.0

        dists = []
        for ti, tm in train_data:
            d = sum((a - b) ** 2 for a, b in zip(inputs_new, ti))
            dists.append((d ** 0.5, tm))

        dists.sort(key=lambda x: x[0])
        k = max(1, min(len(dists), len(train_data) // 2))
        return sum(m for _, m in dists[:k]) / k

    def strategy_random():
        """Pick rows uniformly at random."""
        import random
        chosen = []
        while len(chosen) < 50:
            i = random.randint(0, len(rows) - 1)
            if i not in chosen:
                chosen.append(i)
        return chosen

    def strategy_spot():
        """Pick rows flagged by spot() as suspicious."""
        bad = spot(header, rows)
        # Also include a few random ones to reach up to 50
        import random
        chosen = list(bad)
        while len(chosen) < 50:
            i = random.randint(0, len(rows) - 1)
            if i not in chosen:
                chosen.append(i)
        return chosen

    def strategy_score():
        """Pick rows with highest score (greedy)."""
        scored_rows = [(i, score_row(rows[i])) for i in range(len(rows))]
        scored_rows.sort(key=lambda x: -x[1])
        chosen = [pos for pos, _ in scored_rows[:50]]
        return chosen

    # Run all three strategies
    tried = ["random", "spot", "score"]
    results = {}
    for name in tried:
        if name == "random":
            results[name] = strategy_random()
        elif name == "spot":
            results[name] = strategy_spot()
        else:
            results[name] = strategy_score()

    # Evaluate each chosen row using label (true goal values)
    best_strategy = None
    best_row = None
    best_score_val = -1e9

    for name, positions in results.items():
        for pos in positions:
            true_mre = float(label(pos))
            if true_mre < best_score_val:
                best_score_val = true_mre
                best_strategy = name
                best_row = pos

    return {
        "winner": best_strategy,
        "row": best_row,
        "tried": tried,
    }


if __name__ == "__main__":
    import csv

    with open("Health-ClosedIssues0000.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    result = race(header, rows, label)
    print(f"Winner: {result['winner']}, Row: {result['row']}")
