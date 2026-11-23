import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column (YearsAtCompany+) for test rows
    by building a tree on the training data and predicting the mean
    value of the leaf node where the test row lands.
    """
    # Create table from training data
    tbl = ezr.Tbl([header] + train)
    
    # Build a tree to predict ydist (the aggregate goal distance)
    # Note: The prompt asks for the estimate of the FIRST goal column.
    # We identify the first goal column index.
    goal_cols = [c for c in tbl.y]
    first_goal_idx = goal_cols[0].at
    
    # Build the tree
    root = ezr.tree(tbl, tbl.rows)
    
    # For each test row, find the leaf and return the mean of the 
    # first goal column in that leaf.
    results = []
    for row in test:
        leaf_node = ezr.leaf(root, row)
        # Calculate mean of the first goal column in this leaf
        vals = [r[first_goal_idx] for r in leaf_node.rows]
        results.append(sum(vals) / len(vals))
        
    return results

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Split into train and test (80/20)
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test = rows[split:]
    
    # Mask goals in test data
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
        
    # Get predictions
    predictions = guess(header, train, masked_test)
    
    # Print summary
    print("Estimation complete.")
    print(f"Predicted average tenure (YearsAtCompany+) for {len(predictions)} test cases:")
    print(f"Sample prediction: {predictions[0]:.2f} years.")
    
    exit(0)
