import ezr

def guess(header, train, test):
    """
    Estimates the first goal column for each row in 'test' by training
    a tree on 'train' and predicting the mean of the leaf node.
    """
    # Create a table object for the training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Grow a tree on the training data
    node = ezr.tree(train_tbl, train_tbl.rows)
    
    # Calculate mean of the first goal column (index 0) for each leaf
    leaf_means = {}
    for leaf in ezr.leafs(node):
        vals = [r[0] for r in leaf.rows if r[0] != "?"]
        leaf_means[id(leaf)] = sum(vals) / len(vals) if vals else 0.0
        
    results = []
    for row in test:
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
    train_full = all_rows[:split_idx]
    test_full = all_rows[split_idx:]
    
    # Halve the training set size to simulate "halving the forecaster"
    train_half = train_full[:len(train_full) // 2]
    
    # Mask the goals in the test set
    test_masked = [["?" if i < 3 else val for i, val in enumerate(row)] for row in test_full]
    
    # Get predictions for both scenarios
    preds_full = guess(header, train_full, test_masked)
    preds_half = guess(header, train_half, test_masked)
    
    # Calculate MAE for both
    actuals = [row[0] for row in test_full]
    mae_full = sum(abs(p - a) for p, a in zip(preds_full, actuals)) / len(actuals)
    mae_half = sum(abs(p - a) for p, a in zip(preds_half, actuals)) / len(actuals)
    
    print("Customer Query: If I halve the size of the forecaster to save run time, how much worse do the forecasts get?")
    print(f"Analysis: Training on {len(train_full)} rows yields an MAE of {mae_full:.4f}.")
    print(f"Training on {len(train_half)} rows yields an MAE of {mae_half:.4f}.")
    print(f"The performance degradation is {mae_half - mae_full:.4f} in absolute error.")
    
    exit(0)
