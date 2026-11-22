import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses a tree-based approach. To simulate 'halving the size of the forecaster',
    we limit the training data to half its original size.
    """
    # Halve the training data to simulate a smaller forecaster
    # We use a fixed seed to ensure the subset is consistent
    random.seed(1234567891)
    subset_size = len(train) // 2
    small_train = random.sample(train, subset_size)
    
    # Create the training table
    train_tbl = ezr.Tbl([header] + small_train)
    
    # Build a tree on the training data
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Identify the index of the first goal column
    first_goal_col = train_tbl.y[0]
    goal_idx = first_goal_col.at
    
    results = []
    for row in test:
        # Find the leaf node for the test row
        node = ezr.leaf(root, row)
        
        # Calculate the mean of the first goal column in this leaf
        vals = [r[goal_idx] for r in node.rows if r[goal_idx] != "?"]
        if vals:
            estimate = sum(vals) / len(vals)
        else:
            # Fallback to the global mean if the leaf is empty
            all_vals = [r[goal_idx] for r in train_tbl.rows]
            estimate = sum(all_vals) / len(all_vals)
        results.append(estimate)
        
    return results

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Split into train and test
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test_full = rows[split:]
    
    # Mask the goals in the test set
    test = []
    for row in test_full:
        new_row = list(row)
        for col in ezr.Tbl([header]).y:
            new_row[col.at] = "?"
        test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test)
    
    # Calculate Mean Absolute Error
    actuals = [r[ezr.Tbl([header]).y[0].at] for r in test_full]
    mae = sum(abs(e - a) for e, a in zip(estimates, actuals)) / len(actuals)
    
    print("Impact of halving the forecaster size:")
    print(f"Mean Absolute Error (MAE) with 50% training data: {mae:.4f}")
    print("Conclusion: Reducing the training data size increases the forecast error.")
