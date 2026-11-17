import ezr
from step01 import remember


def guess(header, train, test):
    """Estimate the first goal column for each test row."""
    tbl = ezr.Tbl([header] + train)
    node = ezr.tree(tbl, tbl.rows)

    def predict(r):
        return ezr.leaf(node, r).mu

    return [predict(row) for row in test]


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__), "Health-ClosedIssues0000.train.csv")
    rows = list(ezr.csv(path))
    header = rows[0]
    data_rows = rows[1:]

    mid = len(data_rows) // 2
    train_data = data_rows[:mid]
    test_data = data_rows[mid:]

    predictions = guess(header, train_data, test_data)

    print(f"Predicted {len(predictions)} ydist values for the first goal column:")
    for i, p in enumerate(predictions):
        print(f"  Row {i}: {p:.4f}")
