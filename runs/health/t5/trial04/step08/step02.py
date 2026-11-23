import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    Uses a tree-based ranker to find the nearest neighbors in the training set
    and returns the average MRE- of those neighbors.
    """
    # Create a table for training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data to act as a predictor
    # The tree partitions the space; we use the leaf's mean for the first goal
    node = ezr.tree(train_tbl, train_tbl.rows)
    
    # Identify the index of the first goal column (MRE-)
    # Based on the header, MRE- is at index 0
    goal_idx = 0
    
    predictions = []
    for row in test:
        # Walk the tree to find the leaf containing similar rows
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        # We use the rows stored in the leaf node
        vals = [r[goal_idx] for r in leaf_node.rows if r[goal_idx] != "?"]
        if vals:
            predictions.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean if leaf is empty or data is missing
            all_vals = [r[goal_idx] for r in train if r[goal_idx] != "?"]
            predictions.append(sum(all_vals) / len(all_vals))
            
    return predictions

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Split into train (80%) and test (20%)
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test_full = rows[split:]
    
    # Prepare test rows by masking the goal columns
    # Goals are columns ending in + or -
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    test_masked = []
    for row in test_full:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test_masked.append(new_row)
        
    # Get predictions
    preds = guess(header, train, test_masked)
    
    # Print a sample for the customer
    print("Forecasts for the first goal (MRE-):")
    for i in range(min(5, len(preds))):
        actual = test_full[i][0]
        print(f"Row {i}: Predicted MRE = {preds[i]:.3f}, Actual MRE = {actual:.3f}")
    
    print(f"\nCompleted estimation for {len(preds)} rows.")
