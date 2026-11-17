def remember(header, rows):
    """Return indices of staff who stay unusually long (low attrition)."""
    # Identify goal columns: names ending in '+' are to maximise; '-' minimise.
    goals = [header[i] for i in range(len(header)) if header[i][-1] in '+-']

    def score(row):
        s = 0.0
        for col_name in goals:
            idx = header.index(col_name)
            v = row[idx]
            goal_col = header[header.index(col_name)]
            # Determine goal direction from column name ending
            if goal_col[-1] == '+':
                target = 1.0
            else:
                target = 0.0
            s += abs(v - target)
        return s

    scored = [(score(r), i) for i, r in enumerate(rows)]
    scored.sort(key=lambda x: x[0])
    n = len(scored)
    top_k = max(1, int(n * 0.05))
    return [idx for _, idx in scored[:top_k]]


if __name__ == "__main__":
    import csv

    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    best_idx = remember(header, rows)
    print(f"Top {len(best_idx)} staff who stay unusually long:")
    for i in best_idx:
        print(f"  Row {i}: Attrition={rows[i][1]}, YearsAtCompany+={rows[i][-2]}")
