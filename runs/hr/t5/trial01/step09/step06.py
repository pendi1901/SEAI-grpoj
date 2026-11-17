import ezr

def justify(header, rows, row):
    tbl = ezr.Tbl([header] + rows)

    node = ezr.tree(tbl, rows)

    cur = node
    while cur.kids:
        if cur.go(row):
            cur = cur.kids[0]
        else:
            cur = cur.kids[1]
    pred = cur.mu

    actuals = [ezr.ydist(tbl, r) for r in rows]

    better_count = sum(1 for a in actuals if a > pred)
    p = better_count / len(actuals)

    reason = f"Better than {p:.0%} of staff."
    return (p, reason)


if __name__ == "__main__":
    import csv
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    query_row = list(rows[0])
    goal_cols = [header[i] for i in range(len(header)) if header[i][-1] in '+-']
    for col_name in goal_cols:
        idx = header.index(col_name)
        query_row[idx] = "?"

    p, reason = justify(header, rows, query_row)
    print(f"{reason}")
