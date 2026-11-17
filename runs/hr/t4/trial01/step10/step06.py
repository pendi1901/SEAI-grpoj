import pandas as pd
from step01 import remember


def justify(header, rows, row):
    """Return (fraction_better, reason) for a single employee."""

    goals_plus = [h for h in header if h.endswith('+')]
    goals_minus = [h for h in header if h.endswith('-')]

    # Compute global min/max from the known population
    col_min = {}
    col_max = {}
    for r in rows:
        for c in goals_plus:
            v = float(r[c])
            col_max[c] = max(col_max.get(c, -float('inf')), v)
        for c in goals_minus:
            v = float(r[c])
            col_min[c] = min(col_min.get(c, float('inf')), v)

    # Score each known row using the same normalization
    scores = []
    for r in rows:
        s = 0.0
        for c in goals_plus:
            lo, hi = col_min.get(c, -float('inf')), col_max.get(c, -float('inf'))
            rng = (hi - lo) or 1.0
            s += (float(r[c]) - lo) / rng
        for c in goals_minus:
            lo, hi = col_min.get(c, float('inf')), col_max.get(c, float('inf'))
            rng = (hi - lo) or 1.0
            s += (hi - float(r[c])) / rng
        scores.append(s)

    # Estimate the query row's score: substitute "?" goals with population means
    est_row = list(row)
    for c in goals_plus:
        vals = [float(r[c]) for r in rows]
        est_row[c] = sum(vals) / len(vals) if vals else 0.0
    for c in goals_minus:
        vals = [float(r[c]) for r in rows]
        est_row[c] = sum(vals) / len(vals) if vals else 0.0

    # Score the estimated row with the same normalization
    s_query = 0.0
    for c in goals_plus:
        lo, hi = col_min.get(c, -float('inf')), col_max.get(c, -float('inf'))
        rng = (hi - lo) or 1.0
        s_query += (est_row[c] - lo) / rng
    for c in goals_minus:
        lo, hi = col_min.get(c, float('inf')), col_max.get(c, float('inf'))
        rng = (hi - lo) or 1.0
        s_query += (hi - est_row[c]) / rng

    # Fraction of population that the query row beats
    better_count = sum(1 for s in scores if s < s_query)
    p = better_count / len(scores)

    reason = f"Better than {p:.0%} of employees on tenure and satisfaction goals."
    return (p, reason)


if __name__ == "__main__":
    df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv")
    header = list(df.columns)
    rows = [list(row) for row in df.values]

    # Pick a representative employee (first row, with goals filled from population means)
    sample_row = list(rows[0])
    goals_plus = [h for h in header if h.endswith('+')]
    goals_minus = [h for h in header if h.endswith('-')]
    for c in goals_plus:
        vals = [float(r[c]) for r in rows]
        sample_row[c] = sum(vals) / len(vals)
    for c in goals_minus:
        vals = [float(r[c]) for r in rows]
        sample_row[c] = sum(vals) / len(vals)

    p, reason = justify(header, rows, sample_row)
    print(f"Ranking: {p:.0%} of employees are worse off.")
    print(reason)
