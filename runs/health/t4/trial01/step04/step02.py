import csv
import pandas as pd
import numpy as np


def remember(header, rows):
    goals = [h for h in header if h.endswith('-') or h.endswith('+')]
    n = len(rows)
    scores = np.zeros(n)

    for col in goals:
        vals = []
        for row in rows:
            v = float(row[header.index(col)])
            vals.append(v)
        arr = np.array(vals)
        if arr.max() == arr.min():
            scores += 0.5
        else:
            normed = (arr - arr.min()) / (arr.max() - arr.min())
            if col.endswith('-'):
                scores += (1.0 - normed)
            else:
                scores += normed

    threshold_idx = max(1, int(n * 0.05))
    sorted_indices = np.argsort(scores)[::-1]
    return sorted_indices[:threshold_idx].tolist()


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    best_positions = remember(header, rows)
    print(f"Best {len(best_positions)} out of {len(rows)} setups:")
    for pos in best_positions:
        print(
            f"  Row {pos}: MRE={df.iloc[pos]['MRE-']:.4f}, "
            f"ACC={df.iloc[pos]['ACC+']:.4f}, PRED40={df.iloc[pos]['PRED40+']:.4f}"
        )


def guess(header, train, test):
    goals = [h for h in header if h.endswith('-') or h.endswith('+')]

    # Build a lookup: for each goal column, collect the values from training rows.
    # We will use simple nearest-neighbor prediction based on symbolic features only.
    numeric_cols = [c for c in header if c.isupper()]
    symbolic_cols = [c for c in header if not c.isupper() and not c.endswith('-') and not c.endswith('+')]

    def encode_row(row):
        # Return a tuple of (numeric_vals, symbolic_vals) for matching.
        return (tuple(float(row[header.index(c)]) for c in numeric_cols),
                tuple(row[header.index(c)] for c in symbolic_cols))

    train_enc = [encode_row(r) for r in train]
    test_enc = [encode_row(r) for r in test]

    # For each goal column, compute the mean value across training rows.
    n_train = len(train)
    goal_means = {}
    for col in goals:
        vals = []
        for row in train:
            v = float(row[header.index(col)])
            vals.append(v)
        goal_means[col] = np.mean(vals)

    # Simple prediction: use the training mean as a baseline.
    # To improve, we can try to find similar training rows based on symbolic features.
    def predict_for_row(test_row):
        test_enc_tuple = encode_row(test_row)
        best_match_idx = None
        best_dist = float('inf')

        for i in range(n_train):
            train_enc_tuple = train_enc[i]
            # Compare only symbolic columns (numeric may vary, but we use them too for distance).
            dist = 0.0
            for c in header:
                if c.endswith('-') or c.endswith('+'):
                    continue
                tv = test_enc_tuple[header.index(c)]
                trv = train_enc_tuple[header.index(c)]
                # For symbolic, use categorical distance (0 or 1).
                if isinstance(tv, str) and isinstance(trv, str):
                    dist += 0.0 if tv == trv else 1.0
                elif isinstance(tv, float) and isinstance(trv, float):
                    dist += abs(tv - trv) / 100.0  # normalize roughly

            if dist < best_dist:
                best_dist = dist
                best_match_idx = i

        # Return the goal values from the best matching training row.
        result = []
        for col in goals:
            v = float(test_row[header.index(col)])
            return [v]  # We don't know the true value, so we return a placeholder.
            # Actually, we should predict based on the matched row.

    # Let's redo this properly.
    def predict_goals(test_row):
        test_enc_tuple = encode_row(test_row)
        best_match_idx = None
        best_dist = float('inf')

        for i in range(n_train):
            train_enc_tuple = train_enc[i]
            dist = 0.0
            for c in header:
                if c.endswith('-') or c.endswith('+'):
                    continue
                tv = test_enc_tuple[header.index(c)]
                trv = train_enc_tuple[header.index(c)]
                if isinstance(tv, str) and isinstance(trv, str):
                    dist += 0.0 if tv == trv else 1.0
                elif isinstance(tv, float) and isinstance(trv, float):
                    dist += abs(tv - trv) / 100.0

            if dist < best_dist:
                best_dist = dist
                best_match_idx = i

        # Return the goal values from the best matching training row.
        result = []
        for col in goals:
            v = float(train[best_match_idx][header.index(col)])
            result.append(v)
        return result

    predictions = [predict_goals(r) for r in test]
    return predictions


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    # Create a dummy test row with "?" for goals.
    test_row = ["?" for _ in range(len(header))]
    predictions = guess(header, rows, [test_row])
    print(f"Predicted MRE: {predictions[0][0]:.4f}, ACC: {predictions[0][1]:.4f}, PRED40: {predictions[0][2]:.4f}")
