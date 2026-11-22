import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses the tree-based ranker from ezr to predict the outcome.
    """
    # Create the training table
    tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data to learn the relationship
    # between inputs and the goal columns.
    node = ezr.tree(tbl, tbl.rows)
    
    # The first goal column is the first column in tbl.y
    goal_col = tbl.y[0]
    
    results = []
    for row in test:
        # Walk the tree to find the leaf node for this test row
        leaf = ezr.leaf(node, row)
        
        # Estimate the goal value as the mean of that goal in the leaf
        # We need to extract the values of the first goal column from the leaf rows
        vals = [r[goal_col.at] for r in leaf.rows]
        
        # If the goal is numeric, return the mean; if symbolic, return the mode
        if isinstance(goal_col, ezr.Num):
            results.append(sum(vals) / len(vals))
        else:
            # For symbolic, return the most frequent (mode)
            results.append(max(set(vals), key=vals.count))
            
    return results

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Prepare a train/test split
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test = rows[split:]
    
    # Mask the goals in the test set to simulate "day one"
    # Goals are columns ending in + or -
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_test = []
    for row in test:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        masked_test.append(new_row)
    
    # Get predictions
    predictions = guess(header, train, masked_test)
    
    # Print a summary for the customer
    print("Prediction Analysis: Estimating 'YearsAtCompany+' for new hires.")
    print(f"Processed {len(test)} test cases.")
    print(f"Sample prediction: New hire expected to stay {predictions[0]:.1f} years.")
    print("-" * 60)
    print("The model uses decision trees to map initial employee attributes")
    print("to expected tenure based on historical performance data.")
    
    exit(0)
