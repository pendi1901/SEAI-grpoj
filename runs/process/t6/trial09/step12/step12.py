import ezr
import step02

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for each test row.
    To simulate requirements changing twice as fast halfway through,
    we weight the training data: the second half of the training data
    is given more influence on the model (by duplicating it).
    """
    # Split training data into two halves
    mid = len(train) // 2
    first_half = train[:mid]
    second_half = train[mid:]
    
    # Weight the second half by duplicating it
    weighted_train = first_half + (second_half * 2)
    
    # Use the logic from step02 to build a model on the weighted data
    # We create a table from the weighted training data
    data = [header] + weighted_train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the weighted training data
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column (Cost-)
    goal_idx = 9
    
    results = []
    for row in test:
        # Find the leaf node for this test row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the goal column for all rows in this leaf
        vals = [r[goal_idx] for r in leaf_node.rows if r[goal_idx] != "?"]
        if vals:
            mean_val = sum(vals) / len(vals)
        else:
            # Fallback to global mean if leaf is empty
            all_vals = [r[goal_idx] for r in weighted_train if r[goal_idx] != "?"]
            mean_val = sum(all_vals) / len(all_vals)
            
        results.append(mean_val)
        
    return results

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    # Split data: 80% train, 20% test
    split_idx = int(len(rows) * 0.8)
    train = rows[:split_idx]
    test_raw = rows[split_idx:]
    
    # Mask goals in test rows
    test = []
    for r in test_raw:
        new_row = r[:]
        # Mask all goal columns (Cost-, Score-, Idle-)
        for i in range(9, 12):
            new_row[i] = "?"
        test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test)
    
    print("Impact Analysis: Requirements changing twice as fast halfway through.")
    print(f"Processed {len(test)} test configurations.")
    print(f"Average estimated Cost-: {sum(estimates)/len(estimates):.4f}")
    print("Note: The model was adjusted to give higher weight to recent data.")
    
    exit(0)
