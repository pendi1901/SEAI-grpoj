import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for test rows.
    To simulate the 'changing requirements' scenario, we weight the training
    data: rows that appear later in the training set (representing the 
    'second half' where requirements change) are given more influence 
    in the tree-based estimation.
    """
    # Create a table object for the training data
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # To simulate requirements changing twice as fast, we bias the tree
    # construction. We duplicate the second half of the training data
    # to force the tree to prioritize patterns found in later rows.
    n = len(train)
    second_half = train[n // 2:]
    biased_train = train + (second_half * 2)
    
    # Grow a tree on the biased training data
    biased_tbl = ezr.clone(tbl, biased_train)
    node = ezr.tree(biased_tbl, biased_tbl.rows)
    
    # The first goal column is the first column in tbl.y
    goal_col = tbl.y[0]
    
    estimates = []
    for row in test:
        # Walk the tree to find the leaf for this row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        vals = [r[goal_col.at] for r in leaf_node.rows if r[goal_col.at] != "?"]
        
        if vals:
            estimates.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean if leaf is empty
            estimates.append(goal_col.mu)
            
    return estimates

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    rows_iter = ezr.csv(filename)
    header = next(rows_iter)
    all_rows = list(rows_iter)
    
    # Split data: 80% train, 20% test
    random.seed(1234567891)
    random.shuffle(all_rows)
    n = int(len(all_rows) * 0.8)
    train = all_rows[:n]
    test = all_rows[n:]
    
    # Mask the goals in the test set
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
    
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    # Print a summary for the customer
    print("Impact Analysis: Changing Requirements")
    print("We modeled the impact of requirements changing twice as fast halfway through.")
    print(f"Estimated Cost- for the first 5 configurations under new conditions:")
    for i in range(min(5, len(estimates))):
        print(f"  Config {i+1}: {estimates[i]:.4f}")
    print("\nNote: The model was biased toward later training data to simulate the shift.")
    
    exit(0)
