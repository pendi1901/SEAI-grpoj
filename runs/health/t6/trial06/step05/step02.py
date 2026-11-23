import ezr
import step01

def guess(header, train, test):
    """
    Estimates the first goal column (MRE-) for test rows.
    Uses a tree-based ranker to find the leaf node for each test row
    and returns the mean value of the first goal column in that leaf.
    """
    # Build a table from training data to define columns and goals
    data = [header] + train
    tbl = ezr.Tbl(data)
    
    # Build a tree on the training data
    node = ezr.tree(tbl, tbl.rows)
    
    # Identify the index of the first goal column (MRE-)
    # Based on the header, MRE- is at index 0
    goal_idx = 0
    
    results = []
    for row in test:
        # Find the leaf node for this test row
        leaf_node = ezr.leaf(node, row)
        
        # Calculate the mean of the first goal column in this leaf
        # We use the training rows that ended up in this leaf
        leaf_rows = leaf_node.rows
        if not leaf_rows:
            # Fallback to global mean if leaf is empty
            vals = [r[goal_idx] for r in train]
        else:
            vals = [r[goal_idx] for r in leaf_rows]
            
        results.append(sum(vals) / len(vals))
        
    return results

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
        
        # Split data: 80% train, 20% test
        split_idx = int(len(all_rows) * 0.8)
        train = all_rows[:split_idx]
        test = all_rows[split_idx:]
        
        # Mask the goals in the test set
        test_masked = []
        for r in test:
            new_row = list(r)
            # Mask all goal columns (those ending in + or -)
            for i, name in enumerate(header):
                if name[-1] in "+-":
                    new_row[i] = "?"
            test_masked.append(new_row)
            
        # Get estimates
        estimates = guess(header, train, test_masked)
        
        # Print a summary
        print(f"Estimated MRE- for {len(estimates)} test rows.")
        print(f"First 5 estimates: {[round(x, 4) for x in estimates[:5]]}")
        
        # Calculate average error for validation
        actuals = [r[0] for r in test]
        avg_err = sum(abs(e - a) for e, a in zip(estimates, actuals)) / len(actuals)
        print(f"Average absolute error on test set: {avg_err:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    
    exit(0)
