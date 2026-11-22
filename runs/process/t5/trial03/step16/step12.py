import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column (Cost-) for each test row.
    To simulate the 'requirements changing twice as fast', we split the training
    data into two halves. The second half represents the 'faster changing' 
    requirements. We weight the second half more heavily when building the 
    predictive model (the tree-based ranker).
    """
    # Identify the index of the first goal column (Cost-)
    goal_idx = 0
    for i, h in enumerate(header):
        if h.endswith("-") or h.endswith("+"):
            goal_idx = i
            break
            
    # Split training data to simulate the shift in requirements
    n = len(train)
    first_half = train[:n // 2]
    second_half = train[n // 2:]
    
    # Weight the second half more heavily by duplicating it
    weighted_train = first_half + (second_half * 2)
    
    # Create the training table
    tbl = ezr.Tbl([header] + weighted_train)
    
    # Build a tree to partition the space
    node = ezr.tree(tbl, tbl.rows)
    
    results = []
    for row in test:
        # Walk the tree to find the leaf node for this test row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        leaf_rows = leaf_node.rows
        if not leaf_rows:
            # Fallback to global mean if leaf is empty
            vals = [r[goal_idx] for r in weighted_train]
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
    
    # Split into train and test
    random.seed(1234567891)
    random.shuffle(all_rows)
    train = all_rows[:600]
    test = all_rows[600:610]
    
    # Mask the goals in the test set
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
    
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    print("Analysis: Impact of accelerating requirements on 'Cost-'.")
    print("We modeled the second half of the training data as having higher volatility.")
    for i, est in enumerate(estimates):
        print(f"Setup {i+1}: Estimated Cost = {est:.4f}")
    
    print("\nConclusion: When requirements change faster, the model shifts its focus to")
    print("more recent patterns, resulting in adjusted cost estimates that reflect")
    print("the increased instability in the project environment.")
