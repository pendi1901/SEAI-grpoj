def blame(header, rows):
    goals_min = [c for c in header if c.endswith('-')]
    goals_max = [c for c in header if c.endswith('+')]

    scored = []
    for row in rows:
        score = sum(float(row[c]) for c in goals_min) + \
                 sum(-float(row[c]) for c in goals_max)
        scored.append((score, row))

    scored.sort()
    worst_rows = [r for _, r in scored[:int(len(scored) * 0.15)]]

    input_cols = [c for c in header if c not in goals_min and c not in goals_max]

    col_scores = {c: [] for c in input_cols}
    for row in worst_rows:
        for c in input_cols:
            val = float(row[c]) if c != 'attrition' else 0.0
            col_scores[c].append(val)

    import math
    def mean(xs): return sum(xs)/len(xs) if xs else 0.0
    def sd(xs):
        m = mean(xs)
        var = sum((x - m)**2 for x in xs)/len(xs) if len(xs)>1 else 0.0
        return math.sqrt(var)

    ranked = sorted(col_scores.items(), key=lambda kv: abs(mean(kv[1])), reverse=True)
    top_cols = [c for c, _ in ranked[:5]]

    reasons = []
    for col in top_cols:
        if col == 'attrition': continue
        vals = col_scores[col]
        avg_val = mean(vals)
        std_val = sd(vals)
        reasons.append(f"{col} is typically {avg_val:.1f} (±{std_val:.1f}) among the worst-stayers.")

    return reasons


if __name__ == "__main__":
    import csv, math

    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    reasons = blame(header, rows)
    print("What explains short stays:")
    for r in reasons:
        print(f"  - {r}")
