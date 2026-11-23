import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining the justification.
    """
    # Create a table to handle normalization and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goal values for the input 'row' using the tree's leaf mean
    # We build a tree on the known rows to predict the performance of the input
    root = ezr.tree(tbl, tbl.rows)
    leaf_node = ezr.leaf(root, row)
    
    # Calculate the predicted ydist for the input row
    # We use the mean ydist of the leaf node as the estimate
    predicted_ydist = leaf_node.mu
    
    # Calculate ydist for all known rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that are worse than our predicted row
    # (i.e., have a higher ydist)
    better_than_count = sum(1 for d in all_ydists if d > predicted_ydist)
    p = better_than_count / len(rows)
    
    reason = (f"This configuration is estimated to be in the top {int((1-p)*100)}% "
              f"of all possible setups based on its input characteristics.")
    
    return p, reason

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(file_path)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # Pick a sample row to justify (masking its goals)
    sample_idx = 0
    test_row = list(rows[sample_idx])
    goal_indices = [i for i, h in enumerate(header) if h.endswith(('-', '+'))]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Justification for row {sample_idx}:")
    print(f"Rank: {p:.4f} (fraction of rows outperformed)")
    print(f"Reason: {reason}")
