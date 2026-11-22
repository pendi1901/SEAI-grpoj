import ezr
import step01

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses the tree-based ranker from ezr to estimate the performance
    of the first goal column.
    """
    # Create a table from training data to learn the model
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # Grow a tree on the training data
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column
    # The first goal column is the first column ending in '-' or '+'
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            goal_idx = i
            break
            
    # For each test row, find the leaf node and return the mean of the 
    # first goal column at that leaf
    results = []
    for row in test:
        leaf = ezr.leaf(node, row)
        # Calculate the average of the goal column for rows in this leaf
        vals = [r[goal_idx] for r in leaf.rows if r[goal_idx] != "?"]
        if vals:
            results.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean if leaf is empty or has no data
            results.append(tbl.cols[goal_idx].mu)
            
    return results

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # Split data: 80% train, 20% test
    n = len(all_rows)
    split = int(n * 0.8)
    train = all_rows[:split]
    test = all_rows[split:]
    
    # Mask the goals in the test set to simulate the customer's request
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    # Print summary
    print(f"Estimated first goal (Cost-) for {len(estimates)} test cases:")
    print(f"Average estimated cost: {sum(estimates)/len(estimates):.4f}")
    print("-" * 30)
    for i in range(min(5, len(estimates))):
        print(f"Test row {i}: Estimated Cost- = {estimates[i]:.4f}")
        
    exit(0)
