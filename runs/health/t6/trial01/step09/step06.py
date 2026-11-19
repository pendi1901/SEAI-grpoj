import ezr
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a human-readable explanation.
    """
    # Create a table to calculate ydist (distance to ideal)
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goal values for the target row
    # We use the tree-based ranker from step02 to estimate the goals
    # Since the ranker returns a score based on ydist, we use it to compare
    ranker = step02.guess(header, rows, [row])
    
    # Calculate ydist for all rows in the dataset
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # For the target row, we need to estimate its ydist.
    # Since the goal cells are "?", we use the mean ydist of the leaf 
    # node it falls into, which represents the expected performance.
    node = ezr.tree(tbl, rows)
    leaf_node = ezr.leaf(node, row)
    estimated_ydist = leaf_node.mu
    
    # Calculate how many rows are worse than this estimated performance
    # A row is "better" if its ydist is lower.
    # We want to count how many rows have a higher ydist than our estimate.
    worse_count = sum(1 for d in all_ydists if d > estimated_ydist)
    p = worse_count / len(rows)
    
    reason = (f"This configuration is expected to outperform {int(p * 100)}% "
              "of all known setups based on its input parameters.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_iter = ezr.csv(filename)
    header = next(data_iter)
    rows = list(data_iter)
    
    # Pick a sample row to justify (e.g., the 100th row)
    target_row = list(rows[100])
    # Mask the goals
    for i, name in enumerate(header):
        if name[-1] in "+-!":
            target_row[i] = "?"
            
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification for row 100:")
    print(f"Score (p): {p:.4f}")
    print(f"Reason: {reason}")
