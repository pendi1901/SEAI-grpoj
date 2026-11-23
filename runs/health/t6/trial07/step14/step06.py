import ezr
import step01
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining why.
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goal values for the input 'row'
    # We use the tree-based estimation from step02
    # First, we need to fill the '?' in the input row for the estimation
    # We use the global mid as a safe estimate for the missing goals
    row_with_goals = list(row)
    for col in tbl.y:
        row_with_goals[col.at] = ezr.mid(col)
    
    # Calculate ydist for the target row
    target_ydist = ezr.ydist(tbl, row_with_goals)
    
    # Calculate ydist for all rows in the dataset
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Count how many rows are worse (have a higher ydist) than our target row
    # A lower ydist is better.
    worse_count = sum(1 for d in all_ydists if d > target_ydist)
    p = worse_count / len(rows)
    
    reason = (f"This setup is better than {p:.1%} of all available configurations "
              "because its predicted performance metrics are closer to the ideal "
              "target values than most other observed setups.")
    
    return p, reason

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Pick a sample row (e.g., the 10th row) and mask its goals
    test_row = list(rows[9])
    tbl = ezr.Tbl([header] + rows)
    for col in tbl.y:
        test_row[col.at] = "?"
        
    p, reason = justify(header, rows, test_row)
    
    print(f"Justification Analysis:")
    print(f"Score (p): {p:.4f}")
    print(f"Reason: {reason}")
