import csv


def guess(header, train, test):
    """Estimate the first goal column for each test row using nearest-neighbour on training data."""
    # Identify columns: upper-case = numeric, lower-case = symbolic
    is_numeric = [c[0].isupper() for c in header]

    # Find the first goal column (one ending in '-' or '+')
    goal_col_idx = None
    for i, c in enumerate(header):
        if c.endswith('-') or c.endswith('+'):
            goal_col_idx = i
            break

    def to_float(cell):
        try:
            return float(cell)
        except (ValueError, TypeError):
            return 0.0

    # Precompute training distances using only non-goal numeric columns
    train_data = []
    for row in train:
        vals = [to_float(row[i]) if is_numeric[i] else row[i] for i in range(len(header))]
        train_data.append(vals)

    def distance(a, b):
        d = 0.0
        for i in range(len(header)):
            if not is_numeric[i]:
                continue
            av = a[i]
            bv = b[i]
            if isinstance(av, float) and isinstance(bv, float):
                d += (av - bv) ** 2
        return d

    def predict(row):
        best_dist = float('inf')
        best_val = None
        for i in range(len(train)):
            td = train_data[i]
            if row[goal_col_idx] == "?":
                # skip goal column in distance
                continue
            dist = 0.0
            for j in range(len(header)):
                if not is_numeric[j]:
                    continue
                if j == goal_col_idx:
                    continue
                av = td[j]
                bv = row[j]
                if isinstance(av, float) and isinstance(bv, float):
                    diff = av - bv
                    dist += diff * diff
            if dist < best_dist:
                best_dist = dist
                best_val = to_float(row[goal_col_idx])
        return best_val

    results = [predict(row) for row in test]
    return results


if __name__ == "__main__":
    with open("Health-ClosedIssues0000.train.csv") as f:
        reader = csv.reader(f)
        header = next(reader)
        train_rows = []
        for i, row in enumerate(reader):
            if i < 10000:
                train_rows.append(row)

    # Use a small test set from the training data (goals are "?" in real scenario; here we simulate)
    import random
    random.seed(42)
    test_indices = sorted(random.sample(range(len(train_rows)), 50))
    test_rows = [train_rows[i] for i in test_indices]

    # For the __main__ demo, replace "?" goals with actual values from training to show output
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]
    goal_idx_map = {header.index(c): c for c in goal_cols}

    print(f"Estimated first goal ({goal_cols[0]}) for 50 test rows:")
    for i, row in enumerate(test_rows):
        est = guess(header, train_rows, [row])[0]
        actual = float(row[header.index(goal_cols[0])])
        err = abs(est - actual)
        print(f"  Row {i}: estimate={est:.4f}, actual={actual:.4f}, error={err:.4f}")
