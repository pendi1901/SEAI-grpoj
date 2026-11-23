import ezr
import step01

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows.
    Uses the tree-based ranker from ezr to find the leaf node
    containing the most similar training rows and returns the 
    mean of the first goal column in that leaf.
    """
    # Create a table from training data to build the model
    tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    root = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column (Cost-)
    # Based on the header, Cost- is at index 9
    goal_idx = 9
    
    results = []
    for row in test:
        # Walk the tree to find the leaf node for this test row
        leaf_node = ezr.leaf(root, row)
        
        # Calculate the mean of the first goal column in this leaf
        # We use the training rows that ended up in this leaf
        leaf_rows = leaf_node.rows
        if not leaf_rows:
            # Fallback to global mean if leaf is empty
            vals = [r[goal_idx] for r in train]
        else:
            vals = [r[goal_idx] for r in leaf_rows]
            
        results.append(sum(vals) / len(vals))
        
    return results

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split data: 80% train, 20% test
    n_train = int(len(rows) * 0.8)
    train_data = rows[:n_train]
    test_data = rows[n_train:]
    
    # Mask the goals in the test data (Cost-, Score-, Idle-)
    # Indices 9, 10, 11
    masked_test = []
    for r in test_data:
        new_row = list(r)
        new_row[9] = new_row[10] = new_row[11] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train_data, masked_test)
    
    # Print a summary for the customer
    print(f"Estimated Cost- for {len(estimates)} test scenarios:")
    for i in range(min(5, len(estimates))):
        print(f"Scenario {i+1}: {estimates[i]:.4f}")
    
    if len(estimates) > 5:
        print("...")
