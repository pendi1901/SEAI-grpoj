import ezr

def guess(header, train, test):
    """Predict each test row's first goal column from its features."""
    tbl = ezr.Tbl([header] + train)
    node = ezr.tree(tbl, tbl.rows)
    
    predictions = []
    for row in test:
        leaf = ezr.leaf(node, row)
        predictions.append(leaf.mu)
    
    return predictions

if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__) or ".", "Health-ClosedIssues0000.train.csv")
    with open(path, encoding="utf-8-sig") as f:
        lines = [l.strip() for l in f if l.strip()]
    
    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        rows.append([ezr.atom(s) for s in line.split(",")])
    
    predictions = guess(header, rows, [])
    
    print(f"Loaded {len(rows)} training rows.")
    print("Decision tree built on feature columns; goal values predicted from region membership.")
