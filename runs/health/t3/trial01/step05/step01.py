import pandas as pd


def remember(header, rows):
    """Return positions (0-based) of rows whose forecasts are unusually trustworthy."""
    # Goals to minimise: MRE-
    # Goals to maximise: ACC+, PRED40+
    goals = ["MRE-", "ACC+", "PRED40+"]

    best_scores = {}
    for g in goals:
        vals = []
        for r in rows:
            v = float(r[header.index(g)])
            if g.endswith("-"):
                # lower is better -> score = value (smaller = closer to 0)
                vals.append(v)
            else:
                # higher is better -> score = -value (so larger original => smaller score)
                vals.append(-v)

        best_scores[g] = min(vals)

    scored_rows = []
    for i, r in enumerate(rows):
        s = 0.0
        for g in goals:
            v = float(r[header.index(g)])
            if g.endswith("-"):
                s += (v - best_scores[g])
            else:
                s += (-v - best_scores[g])
        scored_rows.append((i, s))

    scored_rows.sort(key=lambda x: x[1])
    n = len(rows)
    top_k = max(1, int(n * 0.05))
    return [pos for pos, _ in scored_rows[:top_k]]


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = df.values.tolist()
    positions = remember(header, rows)
    print(f"Top {len(positions)} trustworthy setups: {positions}")
