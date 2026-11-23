import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses the tree-based ranker to find the leaf node for a test row,
    then returns the mean value of the first goal column in that leaf.
    """
    # Build a table from the training data
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the training data
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column
    # The first goal column is the first column in tbl.y
    goal_col = tbl.y[0]
    goal_idx = goal_col.at
    
    results = []
    for row in test:
        # Walk the tree to find the leaf for this test row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        vals = [r[goal_idx] for r in leaf_node.rows if r[goal_idx] != "?"]
        if not vals:
            # Fallback to global mean if leaf is empty or has no data
            mean_val = sum(r[goal_idx] for r in tbl.rows) / len(tbl.rows)
        else:
            mean_val = sum(vals) / len(vals)
        results.append(mean_val)
        
    return results

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split into train and test (80/20)
    random.seed(1234567891)
    random.shuffle(rows)
    n = int(len(rows) * 0.8)
    train = rows[:n]
    test_full = rows[n:]
    
    # Mask the goals in the test set to simulate "?"
    # Goals are the last 3 columns: Cost-, Score-, Idle-
    test_masked = []
    for row in test_full:
        new_row = list(row)
        new_row[-3] = "?"
        new_row[-2] = "?"
        new_row[-1] = "?"
        test_masked.append(new_row)
        
    # Get estimates for the first goal (Cost-)
    estimates = guess(header, train, test_masked)
    
    # Calculate actuals for comparison
    actuals = [r[-3] for r in test_full]
    
    # Print summary
    print(f"Estimated Cost- for {len(estimates)} test rows.")
    print(f"Sample estimate: {estimates[0]:.4f} (Actual: {actuals[0]:.4f})")
    print(f"Sample estimate: {estimates[1]:.4f} (Actual: {actuals[1]:.4f})")
    print(f"Sample estimate: {estimates[2]:.4f} (Actual: {actuals[2]:.4f})")
