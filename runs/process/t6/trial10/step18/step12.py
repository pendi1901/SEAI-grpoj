import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column ('Cost-') for each row in test.
    To simulate requirements changing twice as fast halfway through,
    we weight the training data: rows that appear later in the training
    set are given more influence on the tree-based estimation.
    """
    # Identify the index of the first goal column (Cost-)
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith("-") or name.endswith("+"):
            goal_idx = i
            break
            
    # To simulate "requirements changing twice as fast", we duplicate 
    # the second half of the training data to increase its influence.
    n = len(train)
    half = n // 2
    weighted_train = train[:half] + (train[half:] * 2)
    
    # Create table from weighted training data
    data = [header] + weighted_train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the weighted training data
    node = ezr.tree(tbl, tbl.rows)
    
    results = []
    for row in test:
        # Walk the tree to find the leaf for this test row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        vals = [r[goal_idx] for r in leaf_node.rows if r[goal_idx] != "?"]
        if vals:
            results.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean if leaf is empty
            all_vals = [r[goal_idx] for r in weighted_train if r[goal_idx] != "?"]
            results.append(sum(all_vals) / len(all_vals))
            
    return results

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    all_rows = list(rows_gen)
    
    # Split: 80% train, 20% test
    n = int(len(all_rows) * 0.8)
    train = all_rows[:n]
    test = all_rows[n:]
    
    # Mask the goals in test rows
    masked_test = []
    for row in test:
        new_row = row[:]
        # Mask all goal columns (last 3)
        new_row[-3:] = ["?", "?", "?"]
        masked_test.append(new_row)
        
    estimates = guess(header, train, masked_test)
    
    print("Simulation: Requirements change twice as fast halfway through.")
    print(f"Estimated average 'Cost-' for test set: {sum(estimates)/len(estimates):.4f}")
    print("The model has been adjusted to prioritize recent data trends.")
    
    exit(0)
