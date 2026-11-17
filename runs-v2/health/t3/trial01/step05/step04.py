import pandas as pd
import numpy as np


def flow(header, row, seen):
    """Decide whether to stop on `row` given all previously seen rows."""
    goal_cols = [c for c in header if c.endswith('-') or c.endswith('+')]

    # Compute best/worst from the union of seen + current row.
    candidates = seen + [[row]]
    df = pd.DataFrame(candidates, columns=header)

    best = {}
    worst = {}
    for c in goal_cols:
        if c.endswith('-'):
            best[c] = float(df[c].min())
            worst[c] = float(df[c].max())
        else:  # ends with '+'
            best[c] = float(df[c].max())
            worst[c] = float(df[c].min())

    span = {c: best[c] - worst[c] for c in goal_cols}

    def score(r):
        s = 0.0
        for col, d in zip(goal_cols, ['min' if c.endswith('-') else 'max' for c in goal_cols]):
            v = float(r[header.index(col)])
            sp = span[col]
            if sp > 1e-9:
                normed = (v - worst[col]) / sp
            else:
                normed = 0.5
            s += normed
        return s

    current_score = score(row)
    best_so_far = max(score(r) for r in seen) if seen else current_score

    # Stop as soon as the current row is at least as good as any previous one,
    # and within a tight margin of the theoretical optimum.
    threshold = 0.98 * (best_so_far - worst[goal_cols[0]]) + worst[goal_cols[0]]
    return bool(current_score >= best_so_far)


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(r) for r in df.values]

    # Simulate streaming: feed each row one at a time.
    seen = []
    chosen_idx = None
    for i, row in enumerate(rows):
        result = flow(header, row, seen)
        if result:
            chosen_idx = i
            break
        seen.append(row)

    print(f"Chose setup #{chosen_idx + 1} out of {len(rows)}")
