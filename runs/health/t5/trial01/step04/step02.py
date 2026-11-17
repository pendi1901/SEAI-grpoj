import ezr


def guess(header, train, test):
    """Estimate MRE (first goal column) for each test row."""
    tbl = ezr.Tbl(zip(header, train))
    node = ezr.tree(tbl, tbl.rows)
    return [ezr.leaf(node, r).mu for r in test]


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "Health-ClosedIssues0000.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    header = lines[0].split(",")
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]
    n = len(rows)
    split = int(n * 0.8)
    train_rows, test_rows = rows[:split], rows[split:]
    preds = guess(header, train_rows, test_rows)
    print(f"Predicted MRE for {len(preds)} test rows:")
    for i, (r, p) in enumerate(zip(test_rows, preds)):
        print(f"  Row {i}: predicted MRE = {p:.4f}")
