import ezr
import step01

def guess(header, train, test):
    """
    Estimates the first goal column for each test row.
    Uses the tree-based ranker from ezr to find the leaf node
    corresponding to the test row and returns the mean of the 
    first goal column in that leaf.
    """
    # Create a table from training data to define column roles
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the training data
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column
    # The first goal column is the first one in tbl.y
    first_goal_col = tbl.y[0]
    goal_idx = first_goal_col.at
    
    results = []
    for row in test:
        # Walk the tree to find the leaf for this test row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        # We use the 'has' dictionary for Sym or 'mu' for Num
        if isinstance(first_goal_col, ezr.Sym):
            # For symbols, return the most frequent value (or a placeholder)
            results.append(ezr.mid(first_goal_col))
        else:
            # For numeric goals, calculate the mean of the values in this leaf
            vals = [r[goal_idx] for r in leaf_node.rows if r[goal_idx] != "?"]
            if vals:
                results.append(sum(vals) / len(vals))
            else:
                # Fallback to global mean if leaf is empty or missing data
                results.append(first_goal_col.mu)
                
    return results

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Split: 80% train, 20% test
    split_idx = int(len(rows) * 0.8)
    train = rows[:split_idx]
    test_raw = rows[split_idx:]
    
    # Mask the goals in the test set as per requirements
    test = []
    goal_indices = [c.at for c in ezr.Tbl([header] + train).y]
    for row in test_raw:
        new_row = list(row)
        for idx in goal_indices:
            new_row[idx] = "?"
        test.append(new_row)
    
    # Get estimates
    estimates = guess(header, train, test)
    
    # Print summary
    print(f"Estimated the first goal column for {len(test)} test rows.")
    print(f"First 5 estimates: {[round(x, 3) if isinstance(x, float) else x for x in estimates[:5]]}")
    print("The model uses decision tree leaves to predict outcomes based on input features.")
