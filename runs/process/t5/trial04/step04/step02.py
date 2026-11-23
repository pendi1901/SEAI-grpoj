import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each row in test.
    Uses the ezr tree to find the leaf node for each test row
    and returns the mean of the first goal column in that leaf.
    """
    # Create table from training data
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the training data
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column
    # The first goal column is the first column with a name ending in '-' or '+'
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    first_goal_idx = goal_indices[0]
    
    results = []
    for row in test:
        # Walk the tree to find the leaf
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        vals = [r[first_goal_idx] for r in leaf_node.rows if r[first_goal_idx] != "?"]
        if not vals:
            # Fallback to global mean if leaf is empty or missing data
            vals = [r[first_goal_idx] for r in train if r[first_goal_idx] != "?"]
            
        results.append(sum(vals) / len(vals))
        
    return results

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        print("Error: File is empty.")
        exit(1)
        
    # Split data: 80% train, 20% test
    random.seed(1234567891)
    random.shuffle(all_rows)
    split = int(len(all_rows) * 0.8)
    train = all_rows[:split]
    test_raw = all_rows[split:]
    
    # Mask goals in test set
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    test = []
    for row in test_raw:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test)
    
    # Print summary
    print("Estimation Results (First Goal Column):")
    print("-" * 40)
    print(f"Estimated average for {len(estimates)} test cases: {sum(estimates)/len(estimates):.4f}")
    print("-" * 40)
    print("Sample estimates:")
    for i in range(min(5, len(estimates))):
        print(f"Row {i+1}: {estimates[i]:.4f}")
        
    exit(0)
