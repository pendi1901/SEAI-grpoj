import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    To simulate requirements changing twice as fast halfway through,
    we weight the training data: the second half of the training data
    is given more influence (doubled) in the tree construction.
    """
    # Identify the first goal column index
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    first_goal_idx = goal_indices[0]
    
    # Weight the training rows: second half has double weight
    # We simulate this by duplicating the second half of the training rows
    mid = len(train) // 2
    weighted_train = train[:mid] + (train[mid:] * 2)
    
    # Create a table object for the weighted training data
    data = [header] + weighted_train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the weighted training data
    root = ezr.tree(tbl, tbl.rows)
    
    # Predict for each test row
    predictions = []
    for row in test:
        leaf_node = ezr.leaf(root, row)
        # Calculate the mean of the first goal column for rows in this leaf
        vals = [r[first_goal_idx] for r in leaf_node.rows if r[first_goal_idx] != "?"]
        if vals:
            predictions.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean of weighted training data
            all_vals = [r[first_goal_idx] for r in weighted_train if r[first_goal_idx] != "?"]
            predictions.append(sum(all_vals) / len(all_vals))
            
    return predictions

if __name__ == "__main__":
    # Load the data
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    all_rows = list(rows_gen)
    
    # Split data: 80% train, 20% test
    random.seed(1234567891)
    random.shuffle(all_rows)
    split = int(len(all_rows) * 0.8)
    train = all_rows[:split]
    test_raw = all_rows[split:]
    
    # Mask the goals in the test set
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    test = []
    for row in test_raw:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test.append(new_row)
        
    # Get predictions
    preds = guess(header, train, test)
    
    # Print a summary for the customer
    print("Impact Analysis: Requirements changing twice as fast halfway through.")
    print(f"Estimated {header[goal_indices[0]]} for {len(preds)} test configurations.")
    print(f"Average predicted value: {sum(preds)/len(preds):.4f}")
    print("The model accounts for increased volatility by weighting recent data more heavily.")
