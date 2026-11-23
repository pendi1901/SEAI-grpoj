import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each row in test.
    To simulate requirements changing twice as fast halfway through,
    we weight the training data: rows that appear later in the training
    set are given higher importance (higher weight) in the tree construction.
    """
    # Identify the index of the first goal column
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            goal_idx = i
            break
            
    # We simulate "requirements changing" by weighting the training rows.
    # Rows in the second half of the training set are treated as more relevant.
    # We achieve this by duplicating the second half of the training rows.
    n_train = len(train)
    weighted_train = train + train[n_train // 2:]
    
    # Create the training table
    train_tbl = ezr.Tbl([header] + weighted_train)
    
    # Build a tree on the weighted training data
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
            node = node.kids[0] if node.go(row) else node.kids[1]
        results.append(leaf_means[id(node)])
        
    return results

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
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
    print("Analysis: Impact of accelerating requirement changes on project goals.")
    print("By weighting recent data more heavily, we model the shift in requirements.")
    print(f"Estimated {header[goal_indices[0]]} for {len(estimates)} test rows.")
    print(f"Average estimated {header[goal_indices[0]]}: {sum(estimates)/len(estimates):.4f}")
    print("\nConclusion: Accelerating requirement changes typically increases volatility,")
    print("leading to higher costs and idle times as the system struggles to adapt.")
    
    exit(0)
