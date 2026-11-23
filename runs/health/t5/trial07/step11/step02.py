import ezr
import random

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses a decision tree to find the leaf containing similar rows
    and returns the mean value of the first goal column in that leaf.
    """
    # Create a table for training data
    train_tbl = ezr.Tbl([header] + train)
    
    # Build a tree on the training data
    # The tree splits based on x-columns to minimize y-distance
    root = ezr.tree(train_tbl, train_tbl.rows)
    
    # Identify the index of the first goal column
    # The first goal column is the first column that is not an X
    # Based on the header: MRE- is the first goal (index 0)
    goal_idx = 0 
    
    results = []
    for row in test:
        # Walk the tree to find the leaf for this test row
        node = ezr.leaf(root, row)
        
        # Calculate the mean of the first goal column in this leaf
        # We use the rows stored in the leaf node
        vals = [r[goal_idx] for r in node.rows if r[goal_idx] != "?"]
        if vals:
            results.append(sum(vals) / len(vals))
        else:
            # Fallback to global mean if leaf is empty or has no valid goals
            all_vals = [r[goal_idx] for r in train_tbl.rows]
            results.append(sum(all_vals) / len(all_vals))
            
    return results

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Split into train and test
    # Use 80% for training, 20% for testing
    random.seed(1234567891)
    random.shuffle(rows)
    split = int(len(rows) * 0.8)
    train = rows[:split]
    test_raw = rows[split:]
    
    # Mask the goals in the test set to simulate "unknown"
    # The goals are the columns ending in + or -
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    test = []
    for row in test_raw:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test.append(new_row)
        
    # Get estimates
    estimates = guess(header, train, test)
    
    # Calculate average error (MRE is the first goal)
    actuals = [r[0] for r in test_raw]
    errors = [abs(e - a) for e, a in zip(estimates, actuals)]
    avg_error = sum(errors) / len(errors)
    
    print(f"Analysis complete.")
    print(f"Estimated average error for the first goal column: {avg_error:.4f}")
    print(f"Sample estimates: {estimates[:5]}")
