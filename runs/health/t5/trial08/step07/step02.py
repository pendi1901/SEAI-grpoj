import ezr

def guess(header, train, test):
    """
    Estimates the first goal column for each row in 'test' by training
    a tree on 'train' and predicting the mean of the leaf node.
    """
    # Create a table object for the training data
    # ezr.Tbl expects an iterable of rows where the first row is the header
    train_tbl = ezr.Tbl([header] + train)
    
    # Grow a tree on the training data
    node = ezr.tree(train_tbl, train_tbl.rows)
    
    # The first goal column is the one at index 0 (MRE-)
    # We need to find the mean value of this column in the leaf node
    # Since ezr.tree uses ydist, we need a way to map back to the raw column value.
    # We can calculate the mean of the first goal column for each leaf.
    
    leaf_means = {}
    for leaf in ezr.leafs(node):
        # Calculate mean of the first goal column (index 0) for this leaf
        vals = [r[0] for r in leaf.rows if r[0] != "?"]
        leaf_means[id(leaf)] = sum(vals) / len(vals) if vals else 0.0
        
    results = []
    for row in test:
        # Walk the test row down to its leaf
        l = ezr.leaf(node, row)
        results.append(leaf_means[id(l)])
        
    return results

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Split: 80% train, 20% test
    split_idx = int(len(all_rows) * 0.8)
    train = all_rows[:split_idx]
    test_full = all_rows[split_idx:]
    
    # Mask the goals in the test set (first 3 columns are goals)
    test_masked = []
    for row in test_full:
        masked_row = ["?" if i < 3 else val for i, val in enumerate(row)]
        test_masked.append(masked_row)
        
    # Get predictions
    predictions = guess(header, train, test_masked)
    
    # Calculate simple error metric (Mean Absolute Error)
    actuals = [row[0] for row in test_full]
    mae = sum(abs(p - a) for p, a in zip(predictions, actuals)) / len(actuals)
    
    print(f"Analysis complete on {len(train)} training rows.")
    print(f"Estimated Mean Absolute Error on {len(test_masked)} test rows: {mae:.4f}")
    print(f"Sample prediction for first test row: {predictions[0]:.4f} (Actual: {actuals[0]:.4f})")
    
    exit(0)
