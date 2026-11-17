import pandas as pd


def remember(header, rows):
    n = len(rows)
    goals_plus = [i for i, h in enumerate(header) if h.endswith('+')]
    goals_minus = [i for i, h in enumerate(header) if h.endswith('-')]

    col_min = {}
    col_max = {}
    for idx in range(n):
        row = rows[idx]
        for c in goals_plus:
            v = float(row[c])
            col_max[c] = max(col_max.get(c, -float('inf')), v)
        for c in goals_minus:
            v = float(row[c])
            col_min[c] = min(col_min.get(c, float('inf')), v)

    scores = []
    for idx in range(n):
        s = 0.0
        rng = {}
        for c in goals_plus:
            lo, hi = col_min.get(c, -float('inf')), col_max.get(c, -float('inf'))
            rng[c] = (hi - lo) or 1.0
            s += (float(rows[idx][c]) - lo) / rng[c]
        for c in goals_minus:
            lo, hi = col_min.get(c, float('inf')), col_max.get(c, float('inf'))
            rng[c] = (hi - lo) or 1.0
            s += (hi - float(rows[idx][c])) / rng[c]
        scores.append(s)

    ranked = sorted(range(n), key=lambda i: scores[i], reverse=True)
    max_ret = max(1, int(n * 0.05))
    return ranked[:max_ret]


if __name__ == "__main__":
    df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    result = remember(header, rows)
    print(f"Top {len(result)} employees who stay unusually long:")
    for pos in result:
        print(
            f"  Row {pos}: YearsAtCompany={df.iloc[pos]['YearsAtCompany+']}, "
            f"YearsInCurrentRole={df.iloc[pos]['YearsInCurrentRole+]}"
        )
