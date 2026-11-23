import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses a tree-based model trained on the provided training data.
    """
    # Create a table object for the training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    # The tree nodes contain the mean of the ydist, but we need 
    # the actual value of the first goal column.
    # We store the mean of the first goal column in each leaf.
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Pre-calculate the mean of the first goal column for each leaf
    # The first goal column is at index 0
    for node in ezr.leafs(root):
        if not node.rows:
            node.first_goal_mean = 0.0
        else:
            vals = [r[0] for r in node.rows]
            node.first_goal_mean = sum(vals) / len(vals)
            
    # For each test row, find its leaf and return the pre-calculated mean
    results = []
    for row in test:
        leaf = ezr.leaf(root, row)
        results.append(leaf.first_goal_mean)
        
    return results

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    all_rows = list(data_iter)
    
    # Split into train and test
    # Use a fixed seed for reproducibility
    random.seed(1234567891)
    random.shuffle(all_rows)
    
    train_size = 600
    train = all_rows[:train_size]
    test = all_rows[train_size:]
    
    # Mask the goals in the test set to simulate the requirement
    # The goals are the first 3 columns (MRE-, ACC+, PRED40+)
    masked_test = []
    for row in test:
        new_row = ["?"] * 3 + row[3:]
        masked_test.append(new_row)
        
    # Get guesses
    predictions = guess(header, train, masked_test)
    
    # Calculate simple error metric (Mean Absolute Error)
    actuals = [row[0] for row in test]
    mae = sum(abs(p - a) for p, a in zip(predictions, actuals)) / len(actuals)
    
    print(f"Analysis complete.")
    print(f"Estimated Mean Absolute Error for the first goal column: {mae:.4f}")
    print(f"Sample prediction: {predictions[0]:.4f} (Actual: {actuals[0]:.4f})")
