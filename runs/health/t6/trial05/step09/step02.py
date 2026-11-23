import ezr

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    Uses a tree-based ranker to find the leaf node for a test row
    and returns the mean of the first goal column in that leaf.
    """
    # Create a table for training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    # The tree splits based on x-columns to group similar rows
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Pre-calculate the mean of the first goal (index 0) for each leaf
    # We store this in the node object for quick lookup
    def cache_leaf_means(node):
        if not node.kids:
            # Calculate mean of the first goal (index 0) for this leaf
            vals = [r[0] for r in node.rows if r[0] != "?"]
            node.first_goal_mean = sum(vals) / len(vals) if vals else 0
        else:
            for kid in node.kids:
                cache_leaf_means(kid)
    
    cache_leaf_means(root)
    
    # For each test row, find its leaf and return the cached mean
    results = []
    for row in test:
        leaf_node = ezr.leaf(root, row)
        results.append(leaf_node.first_goal_mean)
        
    return results

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Split into train (80%) and test (20%)
    split_idx = int(len(all_rows) * 0.8)
    train = all_rows[:split_idx]
    test_raw = all_rows[split_idx:]
    
    # Mask the goals in the test set to simulate unknown forecasts
    test = []
    for row in test_raw:
        masked = [row[i] if i >= len(header) - len(header) + 3 else "?" for i in range(len(row))]
        # The prompt specifies goals are columns 0, 1, 2. Mask them.
        masked[0] = masked[1] = masked[2] = "?"
        test.append(masked)
    
    # Get estimates
    estimates = guess(header, train, test)
    
    # Print a summary
    print(f"Forecast analysis for {len(estimates)} setups:")
    print(f"Average estimated MRE: {sum(estimates)/len(estimates):.4f}")
    print(f"First 5 estimates: {[round(x, 4) for x in estimates[:5]]}")
