import ezr
import step01

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses the tree-based ranker from ezr to find the leaf node 
    containing similar training rows and returns the mean of the 
    first goal column in that leaf.
    """
    # Create a table for the training data
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the training data
    node = ezr.tree(tbl, tbl.rows)
    
    # For each test row, find the leaf and return the mean of the first goal
    results = []
    for row in test:
        leaf_node = ezr.leaf(node, row)
        # Calculate mean of the first goal column (index 0) in this leaf
        goal_col = tbl.y[0]
        vals = [r[goal_col.at] for r in leaf_node.rows]
        mean_val = sum(vals) / len(vals)
        results.append(mean_val)
    return results

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Split data: 80% train, 20% test
    split_idx = int(len(all_rows) * 0.8)
    train = all_rows[:split_idx]
    test_raw = all_rows[split_idx:]
    
    # Mask the goals in the test set to simulate unknown forecasts
    test = []
    for row in test_raw:
        new_row = list(row)
        for col in range(len(header)):
            if header[col][-1] in "+-!":
                new_row[col] = "?"
        test.append(new_row)
    
    # Get estimates
    estimates = guess(header, train, test)
    
    # Print a summary for the customer
    print(f"Forecasted the first goal column for {len(test)} test cases.")
    print(f"Sample estimates: {[round(x, 3) for x in estimates[:5]]}...")
    
    # Compare with actuals
    actuals = [r[0] for r in test_raw]
    error = sum(abs(e - a) for e, a in zip(estimates, actuals)) / len(actuals)
    print(f"Average absolute error of forecasts: {error:.4f}")
