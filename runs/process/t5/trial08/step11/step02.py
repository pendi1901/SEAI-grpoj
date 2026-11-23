import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    We use a tree-based approach: train a tree on the labeled data,
    then for each test row, find the leaf node and return the mean
    of the first goal column for that leaf.
    """
    # Create a table for the training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    # The tree nodes contain the rows that fall into that partition
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Identify the index of the first goal column
    # The first goal column is the first column that is a goal (ends in + or -)
    goal_indices = [c.at for c in train_tbl.y]
    first_goal_idx = goal_indices[0]
    
    results = []
    for row in test:
        # Walk the tree to find the leaf for this test row
        node = ezr.leaf(root, row)
        
        # Calculate the mean of the first goal column in this leaf
        vals = [r[first_goal_idx] for r in node.rows]
        mean_val = sum(vals) / len(vals)
        results.append(mean_val)
        
    return results

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty or missing.")
        exit(1)
        
    # Split data: 80% train, 20% test
    random.seed(1234567891)
    random.shuffle(all_rows)
    split_idx = int(len(all_rows) * 0.8)
    train = all_rows[:split_idx]
    test_full = all_rows[split_idx:]
    
    # Mask the goals in the test set to simulate "unknown"
    # Goals are columns ending in '-' or '+'
    goal_indices = [i for i, name in enumerate(header) if name[-1] in ('-', '+')]
    test_masked = []
    for row in test_full:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test_masked.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test_masked)
    
    # Print a summary for the customer
    print(f"Estimated the first goal column for {len(estimates)} test cases.")
    print(f"Sample estimates (first 5):")
    for i in range(min(5, len(estimates))):
        print(f"  Test row {i+1}: {estimates[i]:.4f}")
        
    exit(0)
