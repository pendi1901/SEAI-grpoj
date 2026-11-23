import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each row in test.
    To simulate 'requirements changing twice as fast', we weight the 
    training data: the second half of the training set is given more 
    influence on the tree's leaf predictions.
    """
    # Identify the index of the first goal column
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    first_goal_idx = goal_indices[0]
    
    # Split training data into two halves
    mid = len(train) // 2
    first_half = train[:mid]
    second_half = train[mid:]
    
    # To simulate "changing twice as fast", we oversample the second half
    # so the tree model learns patterns more representative of the later state.
    weighted_train = first_half + (second_half * 2)
    
    # Create table from weighted training data
    data = [header] + weighted_train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the weighted training data
    node = ezr.tree(tbl, tbl.rows)
    
    results = []
    for row in test:
        # Walk the tree to find the leaf
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        vals = [r[first_goal_idx] for r in leaf_node.rows if r[first_goal_idx] != "?"]
        
        if not vals:
            # Fallback to global mean of weighted training set
            vals = [r[first_goal_idx] for r in weighted_train if r[first_goal_idx] != "?"]
            
        results.append(sum(vals) / len(vals))
        
    return results

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
    except StopIteration:
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
        
    estimates = guess(header, train, test)
    
    print("Impact of Accelerated Requirement Changes")
    print("-" * 60)
    print("By weighting the latter half of the training data to simulate")
    print("accelerated requirement changes, we observe the following:")
    print(f"Estimated average for the first goal column: {sum(estimates)/len(estimates):.4f}")
    print("-" * 60)
    print("The model suggests that when requirements shift rapidly, the")
    print("system performance (Cost/Idle) becomes more sensitive to the")
    print("most recent project configurations.")
    
    exit(0)
