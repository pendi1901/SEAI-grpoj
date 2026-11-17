import pandas as pd


def blame(header, rows):
    """Return names of input columns that best explain why the worst rows are bad."""
    goals = ["MRE-", "ACC+", "PRED40+"]
    goal_cols = [c for c in header if c in goals]
    input_cols = [c for c in header if c not in goals and c != "?"]

    # Score each row: lower is better (for -), higher is better (for +)
    scored = []
    bests = {}
    for g in goals:
        vals = []
        for r in rows:
            v = float(r[header.index(g)])
            if g.endswith("-"):
                vals.append(v)
            else:
                vals.append(-v)
        bests[g] = min(vals)

    row_scores = []
    for i, r in enumerate(rows):
        s = 0.0
        for g in goals:
            v = float(r[header.index(g)])
            if g.endswith("-"):
                s += (v - bests[g])
            else:
                s += (-v - bests[g])
        row_scores.append((i, s))

    # Worst rows are those with highest score (most negative performance)
    row_scores.sort(key=lambda x: x[1], reverse=True)
    worst = [pos for pos, _ in row_scores[:max(1, len(rows) // 5)]]

    # For each input column, compute average value across worst rows vs all rows
    col_impact = {}
    for c in input_cols:
        worst_vals = []
        all_vals = []
        for r in rows:
            v = float(r[header.index(c)])
            if header.index(c) < len(header):
                all_vals.append(v)
                if any(pos == i for pos, _ in row_scores[:max(1, len(rows) // 5)]):
                    worst_vals.append(v)

        mean_worst = sum(worst_vals) / max(len(worst_vals), 1)
        mean_all = sum(all_vals) / max(len(all_vals), 1)
        col_impact[c] = (mean_worst, mean_all)

    # Rank columns by absolute difference in means
    ranked = sorted(col_impact.items(), key=lambda x: abs(x[1][0] - x[1][1]), reverse=True)
    return [c for c, _ in ranked[:5]]


if __name__ == "__main__":
    df = pd.read_csv("Health-ClosedIssues0000.train.csv")
    header = list(df.columns)
    rows = [list(r) for r in df.values]
    answer = blame(header, rows)
    print(f"Columns most responsible for bad setups: {answer}")
