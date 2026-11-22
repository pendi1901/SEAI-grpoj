import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for each test row.
    Uses the tree-based ranker to find the leaf node for each test row
    and returns the mean value of the first goal column in that leaf.
    """
    # Create the training table
    tbl = ezr.Tbl([header] + train)
    
    # Build a tree to partition the space
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column (Cost-)
    # The first goal column is the one at index 9 in the provided header
    goal_idx = 9 
    
    results = []
    for row in test:
        # Walk the tree to find the leaf node for this test row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        # We use the 'n' and 'mu' logic or simply iterate the rows in the leaf
        leaf_rows = leaf_node.rows
        if not leaf_rows:
            # Fallback to global mean if leaf is empty
            vals = [r[goal_idx] for r in train]
            results.append(sum(vals) / len(vals))
        else:
            vals = [r[goal_idx] for r in leaf_rows]
            results.append(sum(vals) / len(vals))
            
    return results

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Split into train and test for demonstration
    random.seed(1234567891)
    random.shuffle(all_rows)
    train = all_rows[:600]
    test = all_rows[600:610]
    
    # Mask the goals in the test set to simulate the requirement
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
    
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    # Print a summary for the customer
    print("Estimating 'Cost-' for test setups:")
    for i, est in enumerate(estimates):
        print(f"Setup {i+1}: Estimated Cost = {est:.4f}")
