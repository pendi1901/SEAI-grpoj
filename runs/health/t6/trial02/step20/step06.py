import ezr
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and 'reason' explains the performance based on the nearest neighbor.
    """
    # Create a table to use ezr's distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the target row using the logic from step02
    # We find the nearest neighbor in x-space to estimate the unknown goals
    best_neighbor = min(rows, key=lambda r: ezr.xdist(tbl, row, r))
    
    # Calculate ydist for the target row (using the estimated goals)
    # and for all rows in the dataset
    target_ydist = ezr.ydist(tbl, best_neighbor)
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that are worse (have higher ydist) than our target
    # A lower ydist is better, so we count how many rows have a higher ydist
    better_than_count = sum(1 for d in all_ydists if d > target_ydist)
    p = better_than_count / len(rows)
    
    reason = (f"This configuration is better than {int(p * 100)}% of all known setups "
              f"because it mimics the behavior of high-performing clusters with a "
              f"predicted performance distance of {target_ydist:.4f}.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Pick a sample row and mask its goals to test the justification
    test_row = list(rows[100])
    goal_indices = [i for i, h in enumerate(header) if h[-1] in "+-"]
    for idx in goal_indices:
        test_row[idx] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Justification Score: {p:.4f}")
    print(f"Reason: {reason}")
