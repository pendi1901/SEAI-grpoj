import ezr

def spot(header, rows):
    """Find rows with wrongly-typed input values."""
    tbl = ezr.Tbl(iter([header] + rows))

    suspicious = []
    for i, r in enumerate(tbl.rows):
        max_z = 0.0
        for col in tbl.x:
            if type(col) is ezr.Num:
                v = r[col.at]
                sd = col.sd
                if sd > 1e-32 and v != "?":
                    z = abs(v - col.mu) / sd
                    max_z = max(max_z, z)

        # A wrongly-typed value is typically far from the column mean
        if max_z > 4.0:
            suspicious.append((i, max_z))

    suspicious.sort(key=lambda x: -x[1])
    return [idx for idx, _ in suspicious[:5]]


if __name__ == "__main__":
    import csv
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [next(reader) for _ in range(1470)]

    result = spot(header, rows)
    print(f"Rows with likely wrong input values (most suspicious first): {result}")
