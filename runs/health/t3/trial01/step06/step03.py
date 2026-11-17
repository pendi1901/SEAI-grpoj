import pandas as pd


def certify(xs, ys):
    """Return True if xs and ys are the same apart from noise."""
    n = min(len(xs), len(ys))
    diffs = [xs[i] - ys[i] for i in range(n)]
    mean_diff = sum(diffs) / n
    std_diff = (sum((d - mean_diff) ** 2 for d in diffs) / max(n - 1, 1)) ** 0.5
    if std_diff < 1e-6:
        return True
    z = abs(mean_diff) / std_diff
    return z < 2.0


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(r) for r in df.values]

    goals = ["MRE-", "ACC+", "PRED40+"]
    input_cols = [c for c in header if c not in goals]
    goal_cols = [header[header.index(g)] for g in goals]

    big_rows = []
    small_rows = []
    for r in rows:
        n_est = float(r[header.index("N_estimators")])
        if n_est >= 50:
            big_rows.append(r)
        else:
            small_rows.append(r)

    def extract_goals(rows):
        out = []
        for r in rows:
            vals = [float(r[header.index(c)]) for c in goal_cols]
            out.append(vals)
        return out

    big_goals = extract_goals(big_rows)
    small_goals = extract_goals(small_rows)

    print(f"Big setups (N_estimators >= 50): {len(big_rows)}")
    print(f"Small setups (N_estimators < 50): {len(small_rows)}")
    print("Certify result:", certify(big_goals, small_goals))
