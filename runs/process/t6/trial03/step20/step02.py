import ezr
import step01

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses the tree-based ranker from ezr to find the leaf mean of the first goal.
    """
    # Create a table from training data to build the model
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # Identify the index of the first goal column
    goal_idx = [i for i, name in enumerate(header) if name.endswith(('-', '+'))][0]
    
    # Build a tree to estimate values
    # We use the tree structure to find the leaf for each test row
    node = ezr.tree(tbl, tbl.rows)
    
    # For each leaf, calculate the mean of the first goal column
    leaf_means = {}
    for leaf in ezr.leafs(node):
        vals = [r[goal_idx] for r in leaf.rows]
        leaf_means[id(leaf)] = sum(vals) / len(vals)
        
    # Predict for each test row by walking the tree
    predictions = []
    for row in test:
        leaf = ezr.leaf(node, row)
        predictions.append(leaf_means[id(leaf)])
        
    return predictions

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split data: 80% train, 20% test
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test = rows[split:]
    
    # Mask the goals in the test set to simulate "unknown"
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    # Print a summary for the customer
    print(f"Estimation complete for {len(estimates)} scenarios.")
    print(f"First goal column ('{header[goal_indices[0]]}') estimates:")
    for i in range(min(5, len(estimates))):
        print(f"Scenario {i+1}: {estimates[i]:.4f}")
    if len(estimates) > 5:
        print("...")
