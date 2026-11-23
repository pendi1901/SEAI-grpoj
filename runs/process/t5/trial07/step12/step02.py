import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each row in test using the 
    average of the leaf node in a decision tree trained on the train set.
    """
    # Create the training table
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    # The tree uses ydist to split, but we need to estimate a specific goal.
    # We will use the leaf's average value for the first goal column.
    # Identify the index of the first goal column
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            goal_idx = i
            break
            
    # Build tree
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Pre-calculate the average of the first goal for each leaf
    leaf_means = {}
    for node in ezr.leafs(root):
        vals = [r[goal_idx] for r in node.rows]
        leaf_means[id(node)] = sum(vals) / len(vals)
        
    # Predict for each test row
    results = []
    for row in test:
        # Walk the tree to find the leaf
        node = root
        while node.kids:
            # Use the node's split logic
            node = node.kids[0] if node.go(row) else node.kids[1]
        results.append(leaf_means[id(node)])
        
    return results

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("pom3a.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Split into train and test (80/20)
    random.seed(1234567891)
    random.shuffle(rows)
    n = len(rows) // 5
    train = rows[n:]
    test = rows[:n]
    
    # Prepare test rows by masking goals
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_test = []
    for r in test:
        new_row = list(r)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    # Print summary
    print("Estimation complete.")
    print(f"Estimated {header[goal_indices[0]]} for {len(estimates)} test rows.")
    print(f"Sample estimate: {estimates[0]:.4f}")
    
    exit(0)
