import sys
sys.path.insert(0, '.')
from step01 import remember


def justify(header, rows, row):
    goal_cols = [c for c in header if c.endswith('-')]
    input_cols = [c for c in header if not c.endswith('-')]

    # Score each complete row by its goals (lower is better).
    n = len(rows)
    scores_rows = []
    for r in rows:
        s = 0.0
        for col in goal_cols:
            v = float(r[header.index(col)])
            s += -v
        scores_rows.append(s)

    # Query row has "?" goals, so estimate its rank from input features only.
    q_s = 0.0
    for col in input_cols:
        v = float(row[header.index(col)])
        q_s += -v

    better_count = sum(1 for s in scores_rows if s > q_s)
    p = better_count / n

    return (p, f"Better than {p:.0%} of setups by structural similarity.")


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("pom3a.train.csv")
    header = list(df.columns)
    rows = [list(r) for _, r in df.iterrows()]

    goal_cols = [c for c in header if c.endswith('-')]
    test_row = list(rows[0])
    for col in goal_cols:
        test_row[header.index(col)] = "?"

    p, reason = justify(header, rows, test_row)
    print(f"Query beats {p:.2%} of setups. {reason}")
