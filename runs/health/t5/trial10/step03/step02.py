import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses a decision tree built on the training data to predict the 
    mean value of the first goal column in the corresponding leaf.
    """
    # Create a table from training data to define columns and goals
    train_data = [header] + train
    tbl = ezr.Tbl(train_data)
    
    # Build a tree using the training rows
    # Note: ezr.tree uses ydist to split. We need a custom leaf predictor
    # for the specific first goal column.
    node = ezr.tree(tbl, tbl.rows)
    
    # Pre-calculate the mean of the first goal column (at index 0) for each leaf
    # to use as our prediction.
    leaf_means = {}
    
    def compute_leaf_means(n):
        if not n.kids:
            # Calculate mean of column 0 for rows in this leaf
            vals = [r[0] for r in n.rows if r[0] != "?"]
            leaf_means[id(n)] = sum(vals) / len(vals) if vals else 0
        else:
            for k in n.kids:
                compute_leaf_means(k)
                
    compute_leaf_means(node)
    
    # Predict for each test row
    predictions = []
    for row in test:
        leaf_node = ezr.leaf(node, row)
        predictions.append(leaf_means[id(leaf_node)])
        
    return predictions

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split into train/test for demonstration
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test_full = rows[split:]
    
    # Mask the goals in test rows to simulate the customer's request
    # Goals are columns where name ends in + or -
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    test_masked = []
    for row in test_full:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test_masked.append(new_row)
        
    # Get predictions
    preds = guess(header, train, test_masked)
    
    # Calculate simple error (MRE) for the first goal
    actuals = [row[0] for row in test_full]
    mre = sum(abs(p - a) / (a + 1e-32) for p, a in zip(preds, actuals)) / len(actuals)
    
    print(f"Analysis complete.")
    print(f"Estimated Mean Relative Error (MRE) for the first goal: {mre:.4f}")
    print(f"Sample prediction for row 0: {preds[0]:.4f} (Actual: {actuals[0]:.4f})")
    
    exit(0)
