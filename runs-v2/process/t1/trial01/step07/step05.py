import csv


def blame(header, rows):
    goal_cols = ['Cost-', 'Score-', 'Idle-']
    input_cols = [c for c in header if c not in goal_cols]

    def parse_row(row):
        result = {}
        ok = True
        for col in input_cols + goal_cols:
            idx = header.index(col)
            val = row[idx]
            if val == '?':
                return None
            try:
                result[col] = float(val)
            except ValueError:
                return None
        return result

    parsed = []
    for row in rows:
        p = parse_row(row)
        if p is not None:
            parsed.append(p)

    # Score each row: lower is better (all goals end in -)
    def score(rec):
        s = 0.0
        for col in goal_cols:
            s += rec[col]
        return s

    scored = [(score(r), r) for r in parsed]
    scored.sort(key=lambda x: x[0])

    # Worst rows are those with highest total cost (sum of goals, since all end in -)
    worst_rows = [r for _, r in scored[len(scored)//2:]]

    if not worst_rows:
        return []

    # For each input column, compute correlation between its value and the row's score
    # Higher score = worse. We want columns that are high when rows are bad.
    n_worst = len(worst_rows)
    n_total = len(parsed)

    col_names = header[:]
    correlations = []
    for col in input_cols:
        vals = [r[col] for r in parsed if isinstance(r[col], (int, float))]
        worst_vals = [r[col] for r in worst_rows if isinstance(r[col], (int, float))]

        mean_all = sum(vals) / len(vals)
        mean_worst = sum(worst_vals) / len(worst_vals)

        num = sum((v - mean_all) * (w - mean_worst) for v, w in zip(vals, worst_vals))
        den = ((sum((v - mean_all)**2 for v in vals)) *
               (sum((w - mean_worst)**2 for w in worst_vals))) ** 0.5)

        corr = num / den if den > 0 else 0.0
        correlations.append((col, corr))

    # Sort by absolute correlation descending; pick top contributors
    correlations.sort(key=lambda x: abs(x[1]), reverse=True)
    return [c for c, _ in correlations[:3]]


if __name__ == "__main__":
    with open('pom3a.train.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [row for row in reader]

    answer = blame(header, rows)
    print("The worst setups are driven by:", ", ".join(answer))
