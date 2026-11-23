import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row by building a tree
    on the training data and predicting the mean of the leaf node.
    """
    # Create a table object using the ezr library
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    node = ezr.tree(train_tbl, train_tbl.rows)
    
    results = []
    for row in test:
        leaf_node = ezr.leaf(node, row)
        goal_col = train_tbl.y[0]
        at = goal_col.at
        
        # Calculate mean of the goal column for rows in this leaf
        vals = [r[at] for r in leaf_node.rows if r[at] != "?"]
        if vals:
            results.append(sum(vals) / len(vals))
        else:
            results.append(goal_col.mu)
            
    return results

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    all_rows = data[1:]
    
    # Split data: 80% train, 20% test
    random.seed(1234567891)
    random.shuffle(all_rows)
    split = int(len(all_rows) * 0.8)
    train_full = all_rows[:split]
    test_raw = all_rows[split:]
    
    # Mask the goals in the test set
    test = []
    for row in test_raw:
        new_row = list(row)
        new_row[0] = "?"
        test.append(new_row)
        
    # 1. Full size forecast
    preds_full = guess(header, train_full, test)
    actuals = [row[0] for row in test_raw]
    err_full = sum(abs(p - a) for p, a in zip(preds_full, actuals)) / len(actuals)
    
    # 2. Halved size forecast
    # We simulate halving the size by taking half the training rows
    train_half = train_full[:len(train_full) // 2]
    preds_half = guess(header, train_half, test)
    err_half = sum(abs(p - a) for p, a in zip(preds_half, actuals)) / len(actuals)
    
    print("Impact of halving the forecaster size:")
    print(f"Average absolute error (Full size): {err_full:.4f}")
    print(f"Average absolute error (Half size): {err_half:.4f}")
    print(f"Performance degradation: {((err_half - err_full) / err_full) * 100:.2f}%")
    
    exit(0)
