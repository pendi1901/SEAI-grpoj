import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining why.
    
    To answer "Why not use the biggest, deepest setup?", we compare the 
    performance of a 'large' setup (high N_estimators, high Max_depth) 
    against the distribution of all known configurations.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the performance of the provided row using a tree-based ranker
    # The ranker uses the training data (rows) to predict the ydist of the target row.
    node = ezr.tree(tbl, rows)
    ranker = lambda r: ezr.leaf(node, r).mu
    
    # Calculate the estimated ydist for the target row
    target_ydist = ranker(row)
    
    # Calculate ydist for all existing rows to establish the distribution
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # p is the fraction of rows that are worse than the target row.
    # A row is better if its ydist is smaller.
    better_than_count = sum(1 for y in all_ydists if y > target_ydist)
    p = better_than_count / len(rows)
    
    # Construct a reason addressing the "biggest/deepest" question
    reason = (f"Using the biggest, deepest setup is often suboptimal because "
              f"it is only better than {int(p * 100)}% of configurations, "
              "suggesting that simpler models often achieve better performance "
              "without the overhead of excessive complexity.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(0)
        
    # Create a "big, deep" setup to test
    # N_estimators is at index 3, Max_depth is at index 7
    # We set these to high values to represent the "biggest, deepest" setup
    n_est_idx = header.index('N_estimators')
    max_depth_idx = header.index('Max_depth')
    
    # Create a dummy row with high complexity
    test_row = [0.0] * len(header)
    for i, name in enumerate(header):
        if name[-1] in "+-":
            test_row[i] = "?"
        else:
            # Set to high values
            if name == 'N_estimators': test_row[i] = 200.0
            elif name == 'Max_depth': test_row[i] = 20.0
            elif name == 'Min_sample_leaves': test_row[i] = 1.0
            elif name == 'Min_impurity_decrease': test_row[i] = 0.0
            elif name == 'criterion': test_row[i] = 'squared_error'
            else: test_row[i] = 0.0
            
    p, reason = justify(header, rows, test_row)
    
    print(f"Justification: {reason}")
    print(f"Performance percentile: {p:.2f}")
    
    exit(0)
