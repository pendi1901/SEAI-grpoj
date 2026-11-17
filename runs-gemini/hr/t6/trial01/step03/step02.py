import ezr
import random

def guess(header, train, test):
    """
    Estimate the first goal column ('YearsAtCompany+') for test rows
    by training a tree on the provided training data.
    """
    # Create a table object from the training data
    # ezr.Tbl expects an iterable of rows including the header
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    # The tree nodes store the mean of the ydist (distance to goals)
    # However, the prompt asks for an estimate of the FIRST goal column.
    # We use the tree to find the leaf, then return the mean of the 
    # first goal column in that leaf.
    
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Pre-calculate the mean of the first goal column for every leaf
    goal_idx = 0
    for c in train_tbl.y:
        if c.txt == "YearsAtCompany+":
            goal_idx = c.at
            break
            
    for node in ezr.leafs(root):
        vals = [r[goal_idx] for r in node.rows if r[goal_idx] != "?"]
        node.goal_mean = sum(vals) / len(vals) if vals else 0
        
    results = []
    for row in test:
        leaf = ezr.leaf(root, row)
        results.append(float(leaf.goal_mean))
    return results

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Split into train and test for demonstration
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test = rows[split:]
    
    # Mask the goals in the test set to simulate "day one"
    goal_indices = [i for i, h in enumerate(header) if h.endswith(("+", "-"))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, masked_test)
    
    # Print summary
    print(f"Analyzed {len(train)} records to estimate tenure.")
    print(f"Estimated tenure for {len(estimates)} test cases.")
    print(f"Example estimate for first test case: {estimates[0]:.2f} years.")
    exit(0)
